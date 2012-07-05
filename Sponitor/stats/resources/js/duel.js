nsta.loadKillPie = function(version, map, type1, type2) {
		var me = this,
			param = this.PARAMS,
			GET = {};
			
		if (version) {
			GET.version = version;
		}
		if (map) {
			GET.map = map;
		}
		if (type1) {
			GET.type1 = type1;
		}
		if (type2) {
			GET.type2 = type2;
		}
		
		$.ajax('/kill/pie', {
			dataType : 'json',
			data : GET,
			success : function(data) {
				data[0].color = '#00cc00';
				data[1].color = '#ff00ff';
				$.plot($("#killChart"), data, me.PIE_CONFIG);
			}
		});
};

nsta.loadWeaponPies = function(version, map, type1, type2) {
		var me = this,
		param = this.PARAMS,
		GET = {};
			
		if (version) {
			GET.version = version;
		}
		if (map) {
			GET.map = map;
		}
		if (type1) {
			GET.type1 = type1;
		}
		if (type2) {
			GET.type2 = type2;
		}
		
		$.ajax('/kill/weapon/pie', {
			dataType : 'json',
			data : GET,
			success : function(data) {
				var weaponEl = $('#WeaponChart').empty();
				
				$.each(data, function(i, val) {
					var el = $('<div>').addClass('LEFT').css({margin : '10px'}).append( $('<h3>').text(val['name']) ),
						stats = val['statistics'],
						chartEl = $('<div>').css({width: 200, height: 200});
						
					el.append(chartEl);
					weaponEl.append(el);
					
					if(stats[0]) {
						stats[0].color = '#00cc00';
					}
	
					if(stats[1]) {
						stats[1].color = '#ff00ff';
					}
					
					$.plot(chartEl, stats, me.PIE_CONFIG)
				});
			}
		});
}
	
nsta.loadPies = function() {
		var param = this.PARAMS;
		
		this.loadKillPie(param.version, param.map, param.type1, param.type2);
		this.loadWeaponPies(param.version, param.map, param.type1, param.type2);
};

nsta.TITLE = "Duel Statistics";

nsta.PIE_CONFIG = {
		series : {
			pie : {
				show : true,
				label : {
					radius : 0.4,
					formatter : function(label, series) {
						return '<div style="font-family:Arial,font-size:11pt;text-align:center;padding:2px;color:#000000;">' + label + '<br/>' + Math.round(series.percent) + '% <br/>(' + series.data[0][1] + ')</div>';
					},
				}
			}
		},
		legend : {
			show : false
		}
};

// Init the app
$(function($) {
	nsta.init();
});
