function EadViewer(params) {

	var objSelf = this;
	this.data = params;
	this.ead = {};
	// define webservice urls
    var webservice_tree = this.data.webservice_tree
    var webservice_ead = this.data.webservice_ead
    var webservice_archives = this.data.webservice_archives
    var webservice_component = this.data.webservice_component
    var pagebrowser_url = this.data.pagebrowser_url

    var STATUS_PUBLISHED = '2'

	this.render = function() {
		/* set the title and stuff of the ead file */
		$.getJSON(webservice_ead.replace("{ead_id}", params.ead), function(data) {
			if (typeof(data.errors)!=="undefined") {
				$("#ead_title").html("EAD " + params.ead + " could not be found");
				objSelf.ready();
				return;
			}
			objSelf.ead = data;
			$.getJSON(webservice_archives.replace("{archive_id}", data.archive_id), function(data) {
				if (data.length == 1) {
					$("#institution_description").append(data[0].institution_description);
					$("#archive").append(data[0].archive_description + " (" + data[0].archive + ")");
				}
			});
			$("#ead_title").html(data.title);
		});

		/* initialize the tree */
		$.ajax({
			url: webservice_tree.replace("{ead_id}", params.ead),
			success: function(data){
				if (data.results.length > 0) {
					var nodeId, xpath
					objSelf.tree = new Tree(data.results);
					objSelf.tree.build($("#" + objSelf.data.tree.htmlElement));
					$("#" + objSelf.data.tree.htmlElement)
						.jstree({
							"themes" : objSelf.data.tree.themes
						})
						.bind('after_open.jstree', function(event, data) {
							xpath = data.rslt.obj.attr('xpath')
							objSelf.openNode(xpath)
							})
						.bind("select_node.jstree", function (event, data) {
							// if we clicked on a link, we open a pagebrowser
							// if (data.rslt.e.target.classList.contains('link_to_pagebrowser')) {
							// 	openPageBrowser(data.rslt.obj.find('a.link_to_pagebrowser').attr("href"))
							// 	return
							// }
							if (data.inst.is_leaf(data.rslt.obj)) {
								// do nothing if it is a leaf
								// (it should not even be clickable, really
								return
							}
							if (data.inst.is_open(data.rslt.obj)) {
								data.inst.close_node(data.rslt.obj);
								return
							} else {
								// get the data for this component
								xpath = data.rslt.obj.attr('xpath')
	                            objSelf.openNode(xpath)
							};
						})
						.bind("loaded.jstree", function (event, data) {
							// open root node on startup
							xpath = objSelf.tree.getRootNode()
							objSelf.openNode(xpath)
						})
					// make jstree object available
					objSelf.jstree = $.jstree._reference($('#' + objSelf.data.tree.htmlElement))
				}
			},
			dataType: "json"
		});
	}

	this.openNode = function(xpath, callback) {
		/* get the data for this component and show it
		 *
		 * callback is a function that is called after the node is opened
		 *
		 * */
		var nodeId, node
		var component_data_url
		var parent_xpath
		var result

		console.log('opening node ' + xpath)

		node = objSelf.jstree._get_node('*[xpath="' + xpath + '"]')

		if (!node) {
			// we asked to open an unknown node
			// this may be simply because the node does not exist, but may also be because of the fact
			// that the node was not loaded yet
			// to cover the second case, we try to load the parents, recursively
			parent_xpath = xpath.split('/').slice(0, -1).join('/')
			if (!parent_xpath) {
				return
			}
			parent_node = objSelf.jstree._get_node('*[xpath="' + xpath + '"]')
			if (parent_node && parent_node.hasClass('loaded')) {
				// the parent node is already loaded and contains no
				// node for xpath - apparently, such a node does not exist
				return false
			}

			objSelf.openNode(parent_xpath,  function(xpath) {
				return function() {
					objSelf.openNode(xpath, callback)}
				}(xpath)
			)
			return

		}
		nodeId = node.attr('id')
		this.tree.setSelected(nodeId);
		this.tree.currentNode = xpath;
		this.tree.expandUpwards(nodeId);

		if (node.hasClass('loaded')) {
			console.log('node is already loaded')
			if (callback) {
				callback()
			}
			return
		}

		// reset the contents of the node
//		$('#' + nodeId + ' ul').html('')
//		$('#' + nodeId + ' .content').html('')

		// add one of those spinning thingies
		busy_node = $('<div class="busy content"></div>')
		$('#' + nodeId).append(busy_node)

		component_data_url = webservice_component.replace("{ead_id}", this.data.ead).replace("{xpath}", xpath)
		$.getJSON(component_data_url, function(data) {
			busy_node.remove()

			// show child nodes in the .subtree element of the current node
			// and the content of this node in the text .content element
		    data = data['results'][0];

			// create the contentNode
			objSelf.addChildData(data, node)
			node.addClass('loaded')
			if (callback) {
				callback()
			}

		},
		"json");
		return true
	}

	this.addChildren = function(children, element) {
		var i, data , node
		node = objSelf.jstree._get_node(element)

		for (i=0;i<children.length;i++) {
			data = children[i]
//			console.log('[' + (i +1) + '/' + children.length + ']')
			if (!node.hasClass('loaded')) {
				this.addChild(data, node)
			}

		}
	}

	this.addChild = function(data, node) {
		/* create a subnode of the current element with the corresponding data */
		var child_node
		if (!Boolean(data.title)) {
//			console.log('child not created because title is empty: @' + data.xpath)
			return
		}

		child_node = objSelf.jstree._get_node('*[xpath="' + data.xpath + '"]')
		if (!child_node) {
			child_node = objSelf.jstree.create_node(node, 10000, data.title)
		}
		child_node.find('a').addClass('title')
		child_node.attr('xpath', data.xpath)
		child_node.attr('id', data.xpath.replace(/\W/g, ''))
		child_node.addClass('node')

		objSelf.addChildData(data, child_node)

		node.attr('loaded', 'true')
	}


	this.addChildData = function(data, child_node, addChildren) {
		/* child_node is a jstree node */

		var title_node, el_link, el_text, el_icon, content_node, new_node

		title_node = child_node.find('a')

		if (data.children && data.children.length > 0) {
			// if we have children, we put the text in a subnode
			// so it will be opened and closed together with the children
            if (child_node.find('ul').length === 0) {
            	child_node.append($('<ul>'))
            }
            child_node.find('ul').html('')
            content_node = $("<li></li>")
            child_node.find('ul').prepend(content_node)
		} else {
			// we put our content_node immediately following the title
			content_node = $("<div>")
			title_node.after(content_node);
			title_node.removeAttr('href')
		}
		content_node.addClass("content");

		if (data.archiveFile) {
			title_node.removeAttr('href')
			child_node.addClass('archiveFile')

			if(data.archiveFile.indexOf("http://")===0) {
				// archiveFile = url => create link
				title_node.attr('target', '_blank').attr('href', data.archiveFile)
			} else {
				title_node.html("<span class='archiveFile'>" + data.archiveFile + "</span> - " + data.title);
			}
			if (data.scopecontent){
				content_node.append($("<div>").addClass("scopecontent").html(data.scopecontent))
			}
            if (data.custodhist){
            	content_node.append($("<div>").addClass("custodhist").html(params.custodhist_header + ': ' + data.custodhist));
            }
            if (data.text) {
            	content_node.append($("<div>").addClass("text").html(data.text.join("<br/>")));
            }
            if (data.description) {
            	content_node.append($("<div>").addClass("description").html(data.description));
            }
            if (data.date) {
            	content_node.append($("<div>").addClass("date").html(data.date));
            }
			if (data.status == STATUS_PUBLISHED) {
				el_link = $("<a>" + this.data.view_archivefile_text + "</a>")
					.addClass('link_to_pagebrowser')
					.addClass('icon')
					.attr('href', '#')
					.attr('onClick', 'return openPageBrowser("' + pagebrowser_url + this.data.ead.replace(/\./g, '-') + '-' + data.archive_id + '-' + data.archiveFile + '/")')
				content_node.append(el_link);
				child_node.addClass("has_link_to_pagebrowser");
			}
		} else {
			// this is not an archivefile - it is a node that just shows some text
			if (data.date){
				content_node.append(
					$('<div>')
						.addClass('component_date')
						.html(data.date)
					)
			}

			if (data.description) {
				content_node.append(
					$('<div>')
						.addClass('component_description')
						.html(data.description.replace(/\n/g, '<br />'))
					)
			}
			if (data.scopecontent){
				content_node.append(
					$('<div>')
						.addClass('scopecontent')
						.html(data.scopecontent.replace(/\n/g, '<br />'))
					)
		    }

			if (data.custodhist) {
				content_node.append(
					$('<div>')
						.addClass('custodhist')
						.html('<span class="header">' + params.custodhist_header + '</span>: ' + data.custodhist.replace(/\n/g, '<br />'))
					)
			}

			if (data.text && data.text.length > 0 && !(data.text.length === 1 && data.text[0] == "")){
				content_node.append(
					$('<div>')
						.addClass('component_text')
						.html(data.text.join("<br/>").replace(/\n/g, '<br />'))
					)
			}

			if (data.archiveFile){
				new_node = $('<div class="component_archiveFile"></div>')
				new_node.html("Archive file: " + data.archiveFile);
				content_node.append(new_node)
			}

		}

		if (content_node.html()){
			content_node.html(content_node.html().replace(/\n/g, '<br />'));
		} else {
			content_node.remove()
		}

		if (data.children && data.children.length > 0) {
			this.addChildren(data.children, child_node)
		}
	}

	this.scrollTo = function(xpath) {
		var element_to_scroll_to
		element_to_scroll_to = $('*[xpath="' + xpath + '"]')
		if (element_to_scroll_to.length) {
            $(document).scrollTop(element_to_scroll_to.offset().top)
//            $('.selected_node').removeClass('selected_node')
//            element_to_scroll_to.addClass('selected_node')
		}
	}



}


function Tree(data) {
	var data = data;
	this.data = data;
	var nodeCounter = 0;
	var hashTable = {};	// hashtable to keep track of relations xpath-espr. => node-ids
	var inverseHashTable = {};	// hashtable to keep track of relations node-ids => xpath-espr.
	this.currentNode = "";

	this.build = function(root) {
		for(var i=0;i<data.length;i++) {
			var subtree = $("<ul></ul>");
			subtree.append(this.createNode(data[i]));
			root.append(subtree);
		}
	}

	this.createNode = function(node) {
		hashTable[node.xpath] = "phtml_" + nodeCounter;
		inverseHashTable["phtml_" + nodeCounter] = node.xpath;
		if (node.title == "") node.title = "No title";
		var rootNode = $('<li id="phtml_' + nodeCounter + '" class="node">' +
			'<a href="#" title="' + node.title.replace('"', "'") + '">' +
			'<span class="title">' + node.title +
			'</span></a>' +
			'</li>');
		var subtree = $('<ul><li class="content created_by_createNode"></li></ul>');
		rootNode.attr('xpath', node.xpath)
		nodeCounter++;
		rootNode.append(subtree);
		return rootNode;
	}

 	this.getRootNode = function() {
 		return data[0].xpath;
 	}

 	this.getNodeTitle = function(xpath) {
 		var nodeId = parseInt(hashTable[xpath].replace("phtml_", ""));
 		return $("#phtml_" + nodeId + " span.title").html();
 	}

 	/* return xpath-expression of next node */
 	this.getNextNodeId = function() {
 		var nodeId = parseInt(this.getCurrentNodeId().replace("phtml_", ""));
 		return "phtml_" + (nodeId + 1);
 	}
 	this.getPreviousNodeId = function() {
 		var nodeId = parseInt(this.getCurrentNodeId().replace("phtml_", ""));
 		return "phtml_" + (nodeId - 1);
 	}

 	/* return id of current node, e.g. 'phtml_13' */
 	this.getCurrentNodeId = function() {
 		return hashTable[this.currentNode];
 	}

 	this.getCurrentXPath = function() {
 		return this.currentNode;
 	}

 	this.getNodeIdByXpath = function(xpath) {
 		return hashTable[xpath];
 	}
 	this.nodeByXpathExists = function(xpath) {
 		return typeof(hashTable[xpath]) !== 'undefined';
 	}

 	this.getXpathByNodeId = function(nodeId) {
 		return inverseHashTable[nodeId];
 	}

 	this.currentNodeIsFirstNode = function() {
 		return hashTable[this.currentNode] == "phtml_0";
 	}

 	this.currentNodeIsLastNode = function() {
 		return hashTable[this.currentNode] == "phtml_" + (nodeCounter - 1);
 	}

 	this.expandUpwards = function(nodeId) {
		var parentId = this.getParentNodeId(nodeId);
		while(parentId !== null) {
			$("#" + parentId).removeClass("jstree-closed").addClass("jstree-open");
			parentId = this.getParentNodeId(parentId);
		}
 	}

 	this.setSelected = function(nodeId) {
		$(".jstree-clicked").removeClass('jstree-clicked');
		$("#" + nodeId + " a:first").addClass('jstree-clicked');
		$("#" + nodeId).removeClass("jstree-closed").addClass("jstree-open");
 	}

 	this.getParentNodeId = function(nodeId) {
 		var parentId = $("#" + nodeId).parent().parent().attr("id");
 		return typeof(parentId) !== "undefined" && parentId.indexOf("phtml_") === 0 ? parentId : null;
 	}

}


jQuery(document).ready(function($) {
	$("#btnSearch").click(function(event){
		event.preventDefault();
		if ($("#contains_text").val().length > 0) {
			search($("#contains_text").val(), 0, RESULTS_PER_PAGE);
		}
	});
});

function showSearch(){
	$("#search_wrapper").show();
	$("#ead_tree").hide();
	$("#tabs .search").addClass("selected");
};

function hideSearch(){
	$("#search_wrapper").hide();
	$("#ead_tree").show();
	$("#tabs .toc").addClass("selected");
	$("#tabs .search").removeClass("selected");
};

function is_array(input){
	return typeof(input)=='object'&&(input instanceof Array);
}

function search(contains_text, start, limit) {

	$.get(search_service_url + "?start=" + start + "&limit=" + limit + "&ead_id=" + ead + "&contains_text=" + contains_text, function(data) {
		var el_result, divTitle, i, j, xpath, title, breadcrumb, title_link, breadcrumbs, el_icon
		var result
		var node_to_open
		var pages, pager, current_page, pagenum
		var breadcrumbs_list
		$("#results").html("<div id='numberOfResults'>" + data.total_results + " results found</div>");
		showSearch();
		for(i=0; i<data.results.length;i++){
			result = data.results[i]
			el_result = $('<div class="result">')
			divTitle = $('<div class="title">').html((start + i+1) +  '. ');
			// find node_to_open & title of result
			node_to_open = "";
			title = "";
			if (result.show_in_tree) {
				// if node is shown in tree, xpath and title are okay
				node_to_open = result.xpath;
				title = result.title;
			} else {
				// if node is not shown in tree, link to the first breadcrumb (breadcrumbs are by definition always present in the tree)
				if (result.breadcrumbs.length>0) {
					breadcrumb = result.breadcrumbs.shift();
					node_to_open = breadcrumb[0];
					title = breadcrumb[1];
				} else {
					// if there are no breadcrumbs, link to the root node
					node_to_open = eadviewer.tree.getRootNode();
					title = result.title;
				}
			}
			title_link = $('<a>').html(title).attr('href', '#')
				.data('xpath', node_to_open)
				.data('scrollTo', result.xpath)
				.click(function(event){
					event.preventDefault();
					hideSearch() // show the tree
					eadviewer.openNode($(this).data("xpath"), function(xpath) {
							return function(){
								eadviewer.scrollTo(xpath)
     							$('*[xpath="' + xpath + '"]').highlight(contains_text)
								}
						}($(this).data('scrollTo'))
						) // open the node at the given location

					});
			divTitle.append(title_link);
			el_result.append(divTitle);

			if (is_array(result.breadcrumbs)) {
				breadcrumbs = $('<div>').addClass('breadcrumbs')
				el_result.append(breadcrumbs)
				breadcrumbs_list = []
				for (j=result.breadcrumbs.length-1;j>=0;j--) {
					xpath = result.breadcrumbs[j][0]
					breadcrumb = $('<a>')
						.addClass('breadcrumb')
						.attr('href', '#')
						.html(result.breadcrumbs[j][1])
						.data("xpath", xpath)
						.click(function(event){
							event.preventDefault();
							hideSearch() // show the tree
							eadviewer.openNode($(this).data("xpath"), function(xpath) {
									return function(){
										eadviewer.scrollTo(xpath)
										debugger;
									}
								}($(this).data("xpath"))
								) // open the node at the given location

							})

					breadcrumbs.append(breadcrumb)
					if (j > 0) {
						breadcrumbs.append(' > ')
					}
//					if (eadviewer.tree.nodeByXpathExists(result.breadcrumbs[j][0])) {
//						breadcrumbs.push('<a class="breadcrumb" href="#" onclick="eadviewer.getComponent(\'' + result.breadcrumbs[j][0] + '\');return false;">' + result.breadcrumbs[j][1] + '</a>');
//					} else {
//						breadcrumbs.push('<span>' + result.breadcrumbs[j][1] + '</span>');
//					}
//					breadcrumbs_list.push(breadcrumb.prop('outerHTML'))
				}
//				breadcrumbs.html(breadcrumbs_list.join(" &gt; ") + '</div>');
			}

			if (is_array(result.snippet)) {
				el_result.append($('<div class="snippet">' + result.snippet.join("... ") + '</div>'));

			}
			if (typeof(result.status)== '2') {
				el_icon = $("<span></span>").addClass("icon");
				el_result.append(el_icon)
			}

			$("#results").append(el_result);
		}
		// paging
		pages = Math.ceil(data.total_results / limit);
		if (pages > 1) {
			pager = $("<div id='pager'></div>");
			current_page = start / RESULTS_PER_PAGE + 1;
			for (pagenum=1;pagenum<=pages;pagenum++) {
				if (pagenum==current_page) {
					pager.append("<span class='page selected'>" + pagenum + "</span>");
				} else {
					pager.append("<a href='#' class='page' onclick='getPage(" + pagenum + ");return false;'>" + pagenum + "</a>");
				}
			}
			$("#results").append(pager);
		}

	});
}
function getPage(page) {
	search($("#contains_text").val(), (page-1) * RESULTS_PER_PAGE, RESULTS_PER_PAGE);
}


/*
 * jQuery Highlight plugin
 *
 * Based on highlight v3 by Johann Burkard
 * http://johannburkard.de/blog/programming/javascript/highlight-javascript-text-higlighting-jquery-plugin.html
 *
 * Code a little bit refactored and cleaned (in my humble opinion).
 * Most important changes:
 *  - has an option to highlight only entire words (wordsOnly - false by default),
 *  - has an option to be case sensitive (caseSensitive - false by default)
 *  - highlight element tag and class names can be specified in options
 *
 * Usage:
 *   // wrap every occurrance of text 'lorem' in content
 *   // with <span class='highlight'> (default options)
 *   $('#content').highlight('lorem');
 *
 *   // search for and highlight more terms at once
 *   // so you can save some time on traversing DOM
 *   $('#content').highlight(['lorem', 'ipsum']);
 *   $('#content').highlight('lorem ipsum');
 *
 *   // search only for entire word 'lorem'
 *   $('#content').highlight('lorem', { wordsOnly: true });
 *
 *   // don't ignore case during search of term 'lorem'
 *   $('#content').highlight('lorem', { caseSensitive: true });
 *
 *   // wrap every occurrance of term 'ipsum' in content
 *   // with <em class='important'>
 *   $('#content').highlight('ipsum', { element: 'em', className: 'important' });
 *
 *   // remove default highlight
 *   $('#content').unhighlight();
 *
 *   // remove custom highlight
 *   $('#content').unhighlight({ element: 'em', className: 'important' });
 *
 *
 * Copyright (c) 2009 Bartek Szopka
 *
 * Licensed under MIT license.
 *
 */

jQuery.extend({
    highlight: function (node, re, nodeName, className) {
        if (node.nodeType === 3) {
            var match = node.data.match(re);
            if (match) {
                var highlight = document.createElement(nodeName || 'span');
                highlight.className = className || 'highlight';
                var wordNode = node.splitText(match.index);
                wordNode.splitText(match[0].length);
                var wordClone = wordNode.cloneNode(true);
                highlight.appendChild(wordClone);
                wordNode.parentNode.replaceChild(highlight, wordNode);
                return 1; //skip added node in parent
            }
        } else if ((node.nodeType === 1 && node.childNodes) && // only element nodes that have children
                !/(script|style)/i.test(node.tagName) && // ignore script and style nodes
                !(node.tagName === nodeName.toUpperCase() && node.className === className)) { // skip if already highlighted
            for (var i = 0; i < node.childNodes.length; i++) {
                i += jQuery.highlight(node.childNodes[i], re, nodeName, className);
            }
        }
        return 0;
    }
});

jQuery.fn.unhighlight = function (options) {
    var settings = { className: 'highlight', element: 'span' };
    jQuery.extend(settings, options);

    return this.find(settings.element + "." + settings.className).each(function () {
        var parent = this.parentNode;
        parent.replaceChild(this.firstChild, this);
        parent.normalize();
    }).end();
};

jQuery.fn.highlight = function (words, options) {
    var settings = { className: 'highlight', element: 'span', caseSensitive: false, wordsOnly: false };
    jQuery.extend(settings, options);

    if (words.constructor === String) {
        words = [words];
    }
    words = jQuery.grep(words, function(word, i){
      return word != '';
    });
    words = jQuery.map(words, function(word, i) {
      return word.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
    });
    if (words.length == 0) { return this; };

    var flag = settings.caseSensitive ? "" : "i";
    var pattern = "(" + words.join("|") + ")";
    if (settings.wordsOnly) {
        pattern = "\\b" + pattern + "\\b";
    }
    var re = new RegExp(pattern, flag);

    return this.each(function () {
        jQuery.highlight(this, re, settings.element, settings.className);
    });
};
