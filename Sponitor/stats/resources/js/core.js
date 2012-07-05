nsta = {
	PARAMS : {},
	
	TITLE : 'My Title',
	
	PIE_CONFIG : {
		series : {
			pie : {
				show : true,
				label : {
					radius : 0.4,
					formatter : function(label, series) {
						return '<div style="font-family:Arial,font-size:11pt;text-align:center;padding:2px;color:#fff;">' + label + '<br/>' + Math.round(series.percent) + '% <br/>(' + series.data[0][1] + ')</div>';
					},
				}
			}
		},
		legend : {
			show : false
		}
	},
	
	BAR_CONFIG : {
		series: {
    		stack: 1,
            lines: { show: false, fill: true, steps: false },
            bars: { show: true, barWidth: 10 }
        }
	},
			
	loadWinPie : function(version, map) {
		var me = this,
			GET = {};
			
		if (version) {
			GET.version = version;
		}
		if (map) {
			GET.map = map;
		}
		
		$.ajax('/win/pie', {
			dataType : 'json',
			data : GET,
			success : function(data) {
				data[0].color = '#0000ff';
				data[1].color = '#ff0000';
				$.plot($("#winChart"), data, me.PIE_CONFIG);
			}
		});
	},
	
	loadKillPie : function(version, map) {
		var me = this,
			GET = {};
			
		if (version) {
			GET.version = version;
		}
		if (map) {
			GET.map = map;
		}
		
		$.ajax('/kill/pie', {
			dataType : 'json',
			data : GET,
			success : function(data) {
				data[0].color = '#0000ff';
				data[1].color = '#ff0000';
				$.plot($("#killChart"), data, me.PIE_CONFIG);
			}
		});
	},
	
	loadAvgLifetime : function(version, map) {
		var me = this,
			GET = {};
			
		if (version) {
			GET.version = version;
		}
		if (map) {
			GET.map = map;
		}
		
		$.ajax('/lifetime', {
			dataType : 'json',
			data : GET,
			success : function(data) {
				var avgDiv = $('#avg-lifetime').empty();
				var tab = $('<table></table>');
				
				$.each(data, function(i, val) {
					tab.append( $('<tr><td>' + val['target_type'] + '</td><td>' + parseInt(val['lifetime_avg']) + '</td></tr>') );
				});
				
				avgDiv.append(tab);
			}
		});
	},
	
	loadWinBar : function(version, map, delta, offset) {
		var me = this,
			GET = {};
			
		if (version) {
			GET.version = version;
		}
		if (map) {
			GET.map = map;
		}
		if (delta) {
			GET.delta = delta;
		}
		if (offset) {
			GET.delta = delta;
		}

		$.ajax('/win/bar', {
			dataType : 'json',
			data : GET,
			success : function(data) {
				data[0].color = '#0000ff';
				data[1].color = '#ff0000';
				$.plot($("#winLengthChart"), data, {
					series : {
						stack : 1,
						lines : {
							show : false,
							fill : true,
							steps : false
						},
						bars : {
							show : true,
							barWidth : 5
						}
					}
				});
			}
		});

	},
	
	loadPies : function() {
		var param = this.PARAMS;
		
		this.loadKillPie(param.version, param.map);
		this.loadWinPie(param.version, param.map);
		this.loadWinBar(param.version, param.map, param.delta, param.offset);
		this.loadAvgLifetime(param.version, param.map);
	},
	
	updateURL : function() {
		var param;
		
		param = $.extend({}, this.PARAMS);
		$('ul.maps a').each(function(index) {
			var href = $(this).attr('href'),
				map = $.deparam.fragment(href)['map'];
							
			if ( map ) {
				param.map = map;
			} else {
				delete param.map;
			}
			
			$(this).fragment(param, 2);
		});
		
		param = $.extend({}, this.PARAMS);
		$('ul.versions a').each(function(index) {
			var href = $(this).attr('href'),
				version = $.deparam.fragment(href)['version'];
				
	
			if ( version ) {
				param.version = version;
			} else {
				delete param.version;
			}
			
			$(this).fragment(param, 2);
		});
		
		param = $.extend({}, this.PARAMS);
		$('p.delta a').each(function(index) {
			var href = $(this).attr('href'),
				delta = $.deparam.fragment(href)['delta'];
				
	
			if ( delta ) {
				param.delta = delta;
			} else {
				delete param.delta;
			}
			
			$(this).fragment(param, 2);
		});
		
		param = $.extend({}, this.PARAMS);
		$('ul.type1 a').each(function(index) {
			var href = $(this).attr('href'),
				type1 = $.deparam.fragment(href)['type1'];
				
	
			if ( type1 ) {
				param.type1 = type1;
			} else {
				delete param.type1;
			}
			
			$(this).fragment(param, 2);
		});
		
		param = $.extend({}, this.PARAMS);
		$('ul.type2 a').each(function(index) {
			var href = $(this).attr('href'),
				type2 = $.deparam.fragment(href)['type2'];
				
	
			if ( type2 ) {
				param.type2 = type2;
			} else {
				delete param.type2;
			}
			
			$(this).fragment(param, 2);
		});
	},
	
	updateTitle : function() {
		var param = this.PARAMS,
			title = this.TITLE;
		
		if (param.version) {
			title += " - " + param.version;
		}
		if (param.map) {
			title += " - " + param.map;
		}
		
		$('#title').text(title);
	}, 
	onHashChange : function(e) {
		var me = e.data.me, 
			param = $.deparam.fragment();
		
		me.PARAMS = param;

		me.updateURL();
		me.updateTitle();
		me.loadPies();
	},
	
	init : function() {
		var me = this
		$(window).bind("hashchange", { me : me }, this.onHashChange);

		$(window).trigger("hashchange");
	}
};
