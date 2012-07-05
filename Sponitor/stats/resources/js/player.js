nsta.loadGeneral = function(low,mid,high) {
	var me = this,
		GET = {};
		
	if (low && mid && high) {
		GET.low = low;
		GET.mid = mid;
		GET.high = high;
	}
	
	$.ajax('/performance/graph', {
		dataType : 'json',
		data : GET,
		success : function(data) {
			data[0].color = '#ff0000';
			data[1].color = '#ffcc00';
			data[2].color = '#ccff00';
			data[3].color = '#00ff00';
			$.plot($("#general"), data, {
				series : {
					stack : 1,
					lines : {
						show : 1,
						fill : 1,
						steps : 0
					}
				}
			});
		}
	});
};

nsta.loadGPU = function() {
	var me = this,
	GET = {};
	
	$.ajax('/gpu', {
		dataType : 'json',
		data : GET,
		success : function(data) {
			$.plot($("#gpu"), data, me.PIE_CONFIG);
		}
	});
};

nsta.loadCPUCore = function() {
	var me = this,
	GET = {};
	
	$.ajax('/cpucore', {
		dataType : 'json',
		data : GET,
		success : function(data) {
			$.plot($("#cpucore"), data, me.PIE_CONFIG);
		}
	});
};

nsta.loadCPUSpeed = function() {
	var me = this,
	GET = {};
	
	$.ajax('/cpuspeed', {
		dataType : 'json',
		data : GET,
		success : function(data) {
			$.plot($("#cpuspeed"), data, me.PIE_CONFIG);
		}
	});
};
	
nsta.loadPies = function() {
	var param = this.PARAMS;
	
	this.loadGeneral(param.low, param.mid, param.high);
	this.loadGPU();
	this.loadCPUSpeed();
	this.loadCPUCore();
};

nsta.TITLE = "Player Statistics";

nsta.PIE_CONFIG = {
		series : {
			pie : {
				show : true,
				label : {
					radius : 1,
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
