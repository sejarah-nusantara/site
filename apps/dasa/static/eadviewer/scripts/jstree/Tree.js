function Tree(data) {
	var data = data;
	this.data = data;
	var nodeCounter = 0;
	var hashTable = {};	// hashtable to keep track of relations xpath-espr. => node-ids 
	this.hashTable = {};	// hashtable to keep track of relations xpath-espr. => node-ids 
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
		this.hashTable[node.xpath] = "phtml_" + nodeCounter;
		inverseHashTable["phtml_" + nodeCounter] = node.xpath;
		if (node.title == "") node.title = "No title";
		var rootNode = $('<li id="phtml_' + nodeCounter + '" class="node"><ins class="jstree-icon">&nbsp;</ins><a href="#" title="' + node.title.replace('"', "'") + '"><ins class="jstree-icon">&nbsp;</ins><span class="title">' + node.title + '</span></a> </li>');
		var subtree = $("<ul></ul>");
		nodeCounter++;
		for(var i=0;i<node.children.length;i++) {
			subtree.append(this.createNode(node.children[i]));
		}
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
 	}
 	
 	this.getParentNodeId = function(nodeId) {
 		var parentId = $("#" + nodeId).parent().parent().attr("id");
 		if (typeof(parentId) === "undefined") {
 			return null;
 		} else {
 			return parentId.indexOf("phtml_") === 0 ? parentId : null; 
 		}
 	}

}
