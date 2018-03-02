// Create viewer
$(document).ready(function(){
	// Create image processor
	var iviewer = $("#viewer").iviewer({
		src: '',
		ui_disabled: true,
		zoom_min: 10
	});
	var iprocessor = new function(){
		instance = this;
		var cvs, ctx, filters = boot = load = true, img = 'resources/images/no-image.png', passes = {}, passCount = 0;
		var iosDevice = navigator.userAgent.match(/(iPod|iPhone|iPad)/);
		var process = function(){
			var pix = new Pixastic(ctx,'/static/iviewer/pixastic/');
			var pass = Object.keys(passes).shift();
			var options = passes[pass];
			delete passes[pass];
			var passPos = passCount-Object.keys(passes).length;
			try{
				pix[pass](options).done(function(){
					if(passPos<passCount){
						process();
					} else {
						finish();
					}
				},function(p){
					$( "#progressBar" ).progressbar("option", "value", Math.round(((p+passPos-1)/passCount)*100));
				});
			} catch(e){
				finish();
			}
		};
		var initCanvas = function(){
			if(iosDevice){
				throw('iOS is not supported');
			}
			var img = $("#image")[0];
			cvs = document.createElement("canvas");
			cvs.width = img.naturalWidth;
			cvs.height = img.naturalHeight;
			ctx = cvs.getContext("2d");
			ctx.drawImage(img, 0, 0);
			$( "#progressBar" ).progressbar("option", "value", 100);
		}
		var finish = function(){
			try{
				$("#viewer>img")[0].src = cvs.toDataURL("image/jpeg");
				for(var i=0;i<instance.controls.length;i++){
					if(instance.auto) instance.controls[i].slider( "option", "value", 0 );
					instance.controls[i].slider( "option", "disabled", false );
				}
				if(!instance.auto) $( "#applyButton" ).button( "option", "disabled", false );
				$( "#resetButton" ).button( "option", "disabled", false );
				instance.running = false;
			} catch(e){
				lockdown();
				instance.running = false;
			}
		}
		var lockdown = function(){
			filters = false;
			if(iosDevice){
				$( ".progress .progress-label" ).text( $( "#panelFailureIOSText" ).html() );
			} else {
				$( ".progress .progress-label" ).text( $( "#panelFailureText" ).html() );
			}
			for(var i=0;i<instance.controls.length;i++){
				instance.controls[i].slider( "option", "value", 0 );
				instance.controls[i].slider( "option", "disabled", true );
			}
			$( "#applyButton" ).button( "option", "disabled", true );
			$( "#autoFilterButton" ).button( "option", "disabled", true );
			$( "#resetButton" ).button( "option", "disabled", true );
			iviewer.iviewer('loadImage', $("#image")[0].src);
		}
		$("#image").on('load',function(){
			try{
				initCanvas();
				iviewer.iviewer('loadImage', cvs.toDataURL("image/jpeg"));
			} catch(e){
				lockdown();
			}
		});
		$("#image").on('error',function(){
			lockdown();
		});
		$("#viewer>img").on('load',function(){
			if(load){
				load = false;
				$( "#loader" ).fadeOut( "slow" );
				$( "#viewer" ).fadeIn( "slow" );
				$( "#fitButton" ).button( "option", "disabled", false );
				$( "#zoomOrgButton" ).button( "option", "disabled", false );
				$( "#zoomInButton" ).button( "option", "disabled", false );
				$( "#zoomOutButton" ).button( "option", "disabled", false );
				$( "#rotateLeftButton" ).button( "option", "disabled", false );
				$( "#rotateRightButton" ).button( "option", "disabled", false );
				$( "#filterPanelButton" ).button( "option", "disabled", false );
				$( "#resolutionButton1" ).button( "option", "disabled", false );
				$( "#resolutionButton2" ).button( "option", "disabled", false );
				$( "#resolutionButton3" ).button( "option", "disabled", false );
				$( "#resetButton" ).button( "option", "disabled", true );
				$( "#autoFilterButton" ).button( "option", "disabled", false );
			}
			if(boot){
				boot = false;
				instance.toggleFilterPanel();
				instance.toggleAutoFilter();
			}
			if(filters) $( ".progress .progress-label" ).text( $( "#panelIdleText" ).html() );
		});
		instance.auto = true;
		instance.running = false;
		instance.reset = function(){
			try{
				if(!instance.running){
					initCanvas();	
					$("#viewer>img")[0].src = cvs.toDataURL("image/jpeg");
					for(var i=0;i<instance.controls.length;i++){
						instance.controls[i].slider( "option", "value", 0 );
						instance.controls[i].slider( "option", "disabled", false );
					}
					$( "#resetButton" ).button( "option", "disabled", true );
				}
			} catch(e){
				lockdown();
			}
		};
		instance.load = function(src){
			if(src) img = src;
			instance.reload();
		}
		instance.reload = function(){
			var attr = '', res = $("#resolutionButton :radio:checked").attr('value');
			$( "#viewer" ).fadeOut( "slow" );
			$( "#loader" ).fadeIn( "slow" );
			load = true;
			$("#image")[0].crossOrigin = "Anonymous";
			if(res && parseInt(res)>0) attr = '?size='+res+'x'+res;
			$("#image")[0].src = img+attr;
		}
		instance.start = function(){
			if(!instance.running){
				var pix;
				instance.running = true;
				$( "#resetButton" ).button( "option", "disabled", true );
				for(var i=0;i<instance.controls.length;i++){
					instance.controls[i].slider( "option", "disabled", true );
					var value = instance.controls[i].slider( "option", "value" );
					if(value != 0){
						switch(instance.controls[i].attr('id')){
							case 'contractSlider':
								if(!passes.brightness) passes.brightness = { brightness:0, contrast:0 };
								passes.brightness.contrast = value/100;
							break;
							case 'brightnessSlider':
								if(!passes.brightness) passes.brightness = { brightness:0, contrast:0 };
								passes.brightness.brightness = value/100;
							break;
							case 'hueSlider':
								if(!passes.hsl) passes.hsl = { hue:0, saturation:0, lightness:0 };
								passes.hsl.hue = value/100;
							break;
							case 'saturationSlider':
								if(!passes.hsl) passes.hsl = { hue:0, saturation:0, lightness:0 };
								passes.hsl.saturation = value/100;
							break;
							case 'lightnessSlider':
								if(!passes.hsl) passes.hsl = { hue:0, saturation:0, lightness:0 };
								passes.hsl.lightness = value/100;
							break;
							case 'sharpenSlider':
								if(value > 0){
									passes.sharpen5x5 = { strength:Math.abs(value)/250 };
								} else {
									passes.blur = { strength:Math.abs(value)/100 };
								}
							break;
						}
					}
				}
				if(!instance.auto) $( "#applyButton" ).button( "option", "disabled", true );
				passCount = Object.keys(passes).length;
				process();
			}
		};
		instance.toggleAutoFilter = function() {
			if($( "#autoFilterButton" ).is(':checked')){
				instance.auto = true;
				if(!instance.running){
					for(var i=0;i<instance.controls.length;i++){
						instance.controls[i].slider( "option", "value", 0 );
					}
				}
				$( "#autoFilterButton" ).button( "option", "icons", { primary: "ui-icon-locked" } );
				$( "#applyButton" ).button( "option", "disabled", true );
			} else {
				instance.auto = false;
				$( "#autoFilterButton" ).button( "option", "icons", { primary: "ui-icon-unlocked" } );
				$( "#applyButton" ).button( "option", "disabled", false );
			}
		}
		instance.toggleFilterPanel = function() {
			if($( "#filterPanelButton" ).is(':checked')){
				$( "#filterPanel" ).slideDown( "slow" );
				$( "#filterControl" ).fadeIn( "slow" );
			} else {
				$( "#filterPanel" ).slideUp( "slow" );
				$( "#filterControl" ).fadeOut( "slow" );
			}
		}
		$( "#resolutionButton" ).buttonset().on( "change", function() {
			instance.reload();
		});
		$("#resolutionButton1").button( { icons: { primary:'ui-icon-radio-off' }, text: false, disabled: true });
		$("#resolutionButton2").button( { icons: { primary:'ui-icon-radio-on' }, text: false, disabled: true });
		$("#resolutionButton3").button( { icons: { primary:'ui-icon-bullet' }, text: false, disabled: true });
		$( "#applyButton" ).button({ icons: {
			primary: "ui-icon-play"
		}, text: false, disabled: true }).on( "click", function() {
			instance.start();
		});
		$( "#autoFilterButton" ).button({ icons: {
			primary: "ui-icon-locked"
		}, text: false, disabled: true }).on( "change", function() {
			instance.toggleAutoFilter(); 
		});
		$( "#resetButton" ).button({ icons: {
			primary: "ui-icon-seek-first"
		}, text: false, disabled: true }).on( "click", function() {
			instance.reset();
		});
		var progressBar = $( "#progressBar" ),
			progressLabel = $( ".progress .progress-label" );
		progressBar.progressbar({
			change: function() {
				progressLabel.text( $( "#panelProcessingText" ).html()+' ' + Math.round(progressBar.progressbar( "value" )) + "%" );
			},
			complete: function() {
				progressLabel.text( $( "#panelReplacingText" ).html() );
			},
			value: 100
		});
		instance.controls = [
			$( "#contractSlider" ).slider({ min:-100, max:100 }).on( "slidestop", function( event, ui ) {
				if(instance.auto) instance.start();
			}),
			$( "#brightnessSlider" ).slider({ min:-100, max:100 }).on( "slidestop", function( event, ui ) {
				if(instance.auto) instance.start();
			}),
			$( "#hueSlider" ).slider({ min:-100, max:100 }).on( "slidestop", function( event, ui ) {
				if(instance.auto) instance.start();
			}),
			$( "#saturationSlider" ).slider({ min:-100, max:100 }).on( "slidestop", function( event, ui ) {
				if(instance.auto) instance.start();
			}),
			$( "#lightnessSlider" ).slider({ min:-100, max:100 }).on( "slidestop", function( event, ui ) {
				if(instance.auto) instance.start();
			}),
			$( "#sharpenSlider" ).slider({ min:-100, max:100 }).on( "slidestop", function( event, ui ) {
				if(instance.auto) instance.start();
			})
		];
	}();
	// Append viewer and controls
	$( "#fitButton" ).button({ icons: {
		primary: "ui-icon-arrow-4-diag"
	}, text: false, disabled: true }).on( "click", function( event, ui ) {
		iviewer.iviewer('fit');
	});
	$( "#zoomOrgButton" ).button({ icons: {
		primary: "ui-icon-search"
	}, text: false, disabled: true }).on( "click", function() {
		iviewer.iviewer('set_zoom', 100);
	});
	$( "#zoomInButton" ).button({ icons: {
		primary: "ui-icon-zoomin"
	}, text: false, disabled: true }).on( "click", function() {
		iviewer.iviewer('zoom_by', 1);
	});
	$( "#zoomOutButton" ).button({ icons: {
		primary: "ui-icon-zoomout"
	}, text: false, disabled: true }).on( "click", function() {
		iviewer.iviewer('zoom_by', -1);
	});
	$( "#rotateLeftButton" ).button({ icons: {
		primary: "ui-icon-arrowreturnthick-1-w"
	}, text: false, disabled: true }).on( "click", function() {
		iviewer.iviewer('angle', -90);
	});
	$( "#rotateRightButton" ).button({ icons: {
		primary: "ui-icon-arrowreturnthick-1-e"
	}, text: false, disabled: true }).on( "click", function() {
		iviewer.iviewer('angle', 90);
	});
	$( "#filterPanelButton" ).button({ icons: {
		primary: "ui-icon-image"
	}, text: false, disabled: true }).on( "change", function() {
		instance.toggleFilterPanel();
	});
	// Initialise the viewer
	var urlParam = new RegExp('[\\?&]image=([^&#]*)').exec(window.location.href);
	if(urlParam){
		instance.load(decodeURIComponent(urlParam[1]));
	} else {
		instance.load();
	}
});