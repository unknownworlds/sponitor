/**
 * Webapp for Natural Selection 2 statistics
 * 
 * created by Marc Delorme (marc@unknownworlds.com)
 * 
 * © Unknownworlds Entertainment 2012
 */

/* ------------------- Configs -----------------*/
var configMenu = [{
    name: 'Win',
    tag: 'win',
    section: 'Game Statistics'
}, {
    name: 'Kill',
    tag: 'kill',
    section: 'Game Statistics'
}, {
    name: 'Lifetime Average',
    tag: 'lifetime',
    section: 'Game Statistics'
},{
    name: 'Start location count',
    tag: 'startlocation',
    section: 'Game Statistics'
}, {
    name: 'Win - Length (Bar)',
    tag: 'winlength',
    section: 'Game Statistics'
}, {
    name: 'Win - Length (Pie)',
    tag: 'winpielength',
    section: 'Game Statistics'
}, {
    name: 'Win - Start distance (Bar)',
    tag: 'windistance',
    section: 'Game Statistics'
}, {
    name: 'Win - Start distance (Pie)',
    tag: 'winpiedistance',
    section: 'Game Statistics'
}, {
    name: 'Duel',
    tag: 'duel',
    section: 'Game Statistics'
}, {
    name: 'Duel - Weapon',
    tag: 'duelweapon',
    section: 'Game Statistics'
}, {
    name: 'GPU',
    section: 'Computer Statistics',
    tag: 'gpu'
}, {
    name: 'CPU Speed',
    section: 'Computer Statistics',
    tag: 'cpuspeed'
}, {
    name: 'CPU Cores',
    section: 'Computer Statistics',
    tag: 'cpucore'
}, {
    name: 'Resolution',
    section: 'Computer Statistics',
    tag: 'resolution'
}, {
    name: 'Performance',
    section: 'Computer Statistics',
    tag: 'performance'
}];

var configMaps = [{
    name: 'ns2_mineshaft'
}, {
    name: 'ns2_tram'
}, {
    name: 'ns2_summit'
}, {
    name: 'ns2_rockdown'
}, {
    name: 'ns2_docking'
}, {
    name: 'ns2_refinery'
}, {
    name: 'ns2_veil'
}];

/* ----------------- Charts Config ------------------ */

var PIE_CONFIG = {
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
};

var PIE_OPTIONS = {
    width : 600,
    height : 500,
    backgroundColor : {
        strokeWidth : 1,
        stroke : '#bbb'
    },
    chartArea : {
        top : '10%',
        left : '10%',
        width : '100%',
        height : '100%'
    }
};

var BAR_OPTIONS = {
    backgroundColor : {
        strokeWidth : 1,
        stroke : '#bbb'
    },
    chartArea : {
        top : '10%',
        left : '10%',
        width : '100%',
        height : '100%'
    },
    isStacked: true
};

/* ----------------- Utils function ------------------ */

var classify = function(str) {
    return str.replace(' ', '-');
}

var appendTmpTo = function(tmp_item, data, to_item) {
    $( to_item ).html( _.template($( tmp_item ).html(), data) );
}

/* ------------------------ Define view ----------------------- */

var StatModel = Backbone.Model.extend({
    defaults: {
        name: 'Test',
        tag: 'notImplemented',
        section: 'Other'
    }
});

var FilterItemModel = Backbone.Model.extend({
    defaults: {
        name: 'default_name',
        group: 'default',
        active: false
    }
});

var StatCollection = Backbone.Collection.extend({
    model: StatModel
});

var FilterItemCollection = Backbone.Collection.extend({
    model: FilterItemModel,
    
    initialize: function(options) {
        if (options && options.url) {
            this.url = options.url;
        }
    },
    
    getActive: function() {
        var actives = [];
        
        _(this.models).each(function(item) {
            if ( item.get('active') ) {
                actives.push( item.get('name') );
                }
            });

            return actives;
        }
    });
 
/* ------------------------ Define view ------------------------ */         
var FilterCheckItemView = Backbone.View.extend({
    tagName: 'span',
    events : {
        'click label': 'toggleItem'
    },
    initialize: function() {
        _.bindAll(this);
        this.render();
    },
    render: function() {
        $(this.$el).html('<input type="checkbox" id="check-' + this.model.get('name') + '" /><label for="check-' + this.model.get('name') + '">' + this.model.get('name') + '</label>');
        return this;
    },
    toggleItem: function(e) {
        if ( $('label', this.el).hasClass('ui-state-active') ) {
            this.model.set('active', true);
        } else {
            this.model.set('active', false);
        }
    }
});

var FilterCheckView = Backbone.View.extend({
    el: $('#filter'),
    initialize: function() {
        _.bindAll(this, 'render');
        this.collection.bind('reset', this.render);
        this.render();
    },
    render: function() {
        var me = this;
        
        $(this.el).empty();

        _(this.collection.models).each(function(item){
            me.appendItem(item);
        }, this);
        
        $(this.el).buttonset();
    },
    appendItem: function(item) {
        var itemView = new FilterCheckItemView({
            model: item
        });
        $(this.el).append(itemView.render().el);
    }
});

var FilterSelectItemView = Backbone.View.extend({
    tagName: 'option',
    initialize: function() {
        _.bindAll(this);
        this.render();
    },
    render: function() {            
        $(this.$el).attr('value', this.model.get('name')).text( this.model.get('name') );
        return this;
    }
});
    
var FilterSelectView = Backbone.View.extend({
    el: $('#filter'),
    events: {
        'change select' : 'onSelect'
    },
    initialize: function() {
        _.bindAll(this);
        this.collection.bind('reset', this.render);
        this.render();
    },
    render: function() {
        var me = this
            selectEl = $('<select>');
        
        $(this.el).empty();
        selectEl.append('<option value="null">All</option>');
        $(this.el).append(selectEl);
        
        _(this.collection.models).each(function(item){
            var group = item.get('group'),
                itemView = new FilterSelectItemView({
                model: item
            });
            
            me.appendGroup(group)
            
            $('optgroup[label=' + group +']',selectEl).append(itemView.render().el);
        }, this);
    },
    appendGroup: function(group) {
        if($('optgroup[label=' + group +']', this.el).length == 0) {
            $('select', this.el).append('<optgroup label="' + group + '"></optgroup>');
        }
    },
    onSelect : function() {
        this.trigger('select');
    },
    getValue : function() {
        var el = $('select option:selected', this.el),
            value = el.attr('value');
        return value === "null" ? null : value;
    }
});

var FilterSelectLocationView = FilterSelectView.extend({
    initialize: function(options) {
        FilterSelectView.prototype.initialize.apply(this);
        
        if (options.maps) {
            this.maps = options.maps;
            this.maps.bind('change', this.onChange);
        }
    },
    
    onChange: function() {
        var GET = {};
         
        // Filter
        if (this.maps && this.maps.getActive().length > 0) {
            GET.map = $.toJSON( this.maps.getActive() );
        }
        
        this.collection.fetch({
            data: GET
        });
    }
});

var FilterView = Backbone.View.extend({
    el: $('#filters-widget'),
    initialize: function(filters) {
        _.bindAll(this);
        
        if (filters) {
            this.filters = filters;
        } else {
            this.filters = {};
        }           
    },
    hide: function() {
        $(this.el).addClass('ui-helper-hidden');
    },
    show: function(list) {
        var me = this;
        
        $(this.el).removeClass('ui-helper-hidden');
        if (list) {
            _(this.filters).each(function(value) {
                $(value.el).addClass('ui-helper-hidden');
            });
            
            _(list).each(function(item) {
                if (me.filters[item]) {
                    $(me.filters[item].el).removeClass('ui-helper-hidden');
                }
            });
        }
    }
})

var StatMenuItemView = Backbone.View.extend({
    tagName : 'li',
    events: {
        'click a': 'selectItem'
    },
    initialize: function() {
        _.bindAll(this);
        this.render()
    },
    selectItem: function() {
        $('li a', $(this.el).parents('.menu-list') ).removeClass('menu-item-on');
        $('a', this.el).addClass('menu-item-on');
    },
    render: function() {
        $(this.el).html('<a href="#' + this.model.get('tag') + '">' + this.model.get('name') + '</a>');
        return this;
    }
});

var MenuView = Backbone.View.extend({
    el: $('#main-menu .menu-list'),
    initialize: function(data) {
        _.bindAll(this);
        
        this.collection = new StatCollection(data.config);
        this.collection.bind('add', this.render);
        this.render();
    },
    render: function() {
        var me = this;
        $(this.el).empty();

        _(this.collection.models).each(function(stat){
            me.appendStat(stat);
        }, this);
        $(this.el).accordion({
            autoHeight : false
        });
    },
    appendStat: function(stat) {
        var section = stat.get('section'),
            statView = new StatMenuItemView({
                model: stat
            });
        
        this.appendSection(section);    
        $('div.menu-' + classify(section) + ' ul', this.el).append(statView.render().el);
    },
    appendSection: function(section) {
        if ( $('h3.menu-' + classify(section), this.el).length == 0 ) {
            $(this.el).append('<h3 class="menu-' + classify(section) + '"><a href="#">' + section + '</a></h3><div class="menu-' + classify(section)+ '"><ul></ul></div>');
        }
    }
});

var ChartView = Backbone.View.extend({
        
    onChange: function() {
        this.clearCharts();
        this.render();
    },
    
    clearCharts: function() {
        _(this.charts).each(function(chart) {
            chart.clearChart();
        });
        this.charts = [];
    },

    remove : function() {
        this.clearCharts();
        
        if (this.versions) {
            this.versions.off('change', this.onChange);
        }
        if (this.maps) {
            this.maps.off('change', this.onChange);
        }
        if (this.type1View) {
            this.type1View.off('select', this.onChange);
        }
        if (this.type2View) {
            this.type2View.off('select', this.onChange);
        }
        if (this.location1View) {
            this.location1View.off('select', this.onChange);
        }
        if (this.location2View) {
            this.location2View.off('select', this.onChange);
        }
        
        this.$el.empty();
    }
});

var PieView = ChartView.extend({
    el: $('#content'),
    initialize : function(options) {
        _.bindAll(this);
        this.charts = [];
        
        if (options.name) {
            this.name = options.name;
        } else {
            console.error('A pie view should have a name');
        }
        if (options.url) {
            this.url = options.url;
        } else {
            console.error('A pie view should have a url');
        }
        if (options.versions) {
            this.versions = options.versions;
            this.versions.bind('change', this.onChange);
        }
        if (options.maps) {
            this.maps = options.maps;
            this.maps.bind('change', this.onChange);
        }
        if (options.type1View) {
            this.type1View = options.type1View;
            this.type1View.bind('select', this.onChange);
        }
        if (options.type2View) {
            this.type2View = options.type2View;
            this.type2View.bind('select', this.onChange);
        }
        if (options.location1View) {
            this.location1View = options.location1View;
            this.location1View.bind('select', this.onChange);
        }
        if (options.location2View) {
            this.location2View = options.location2View;
            this.location2View.bind('select', this.onChange);
        }
        
        this.render();
    },
    
    render : function() {
        var me = this, 
            GET = {};

        // Prepare DOM
        $(this.el).empty();
        appendTmpTo('#pieTmp', {title: this.name}, this.el);

        // Filter
        if (this.versions && this.versions.getActive().length > 0) {
            GET.version = $.toJSON( this.versions.getActive() );
        }
        if (this.maps && this.maps.getActive().length > 0) {
            GET.map = $.toJSON( this.maps.getActive() );
        }
        if (this.type1View ) {
            GET.type1 = this.type1View.getValue();
        }
        if (this.type2View) {
            GET.type2 = this.type2View.getValue();
        }
        if (this.location1View && this.location1View.getValue()) {
            GET.location1 = this.location1View.getValue();
        }
        if (this.location2View && this.location2View.getValue()) {
            GET.location2 = this.location2View.getValue();
        }

        // Render the pie
        $.ajax(this.url, {
            dataType : 'json',
            data : GET,
            success : function(response) {
                var data = new google.visualization.DataTable(),
                    chart = new google.visualization.PieChart( $('.pieChart', me.el)[0] ),
                    options = {};
                
                data.addColumn('string', 'Categories');
                data.addColumn('number', 'Count');
                data.addRows(response.data);
                
                if (response.colors) {
                    options.colors = response.colors;
                }
                _.extend(options, PIE_OPTIONS);
                
                chart.draw(data, options);
                
                me.charts.push(chart);
            }
        });
    }
});

var LifetimeView = ChartView.extend({
    el: $('#content'),
    initialize : function(options) {
        _.bindAll(this);
        this.charts = [];
        
        if (options.name) {
            this.name = options.name;
        } else {
            console.error('A pie view should have a name');
        }
        if (options.url) {
            this.url = options.url;
        } else {
            console.error('A pie view should have a url');
        }
        if (options.versions) {
            this.versions = options.versions;
            this.versions.bind('change', this.onChange);
        }
        if (options.maps) {
            this.maps = options.maps;
            this.maps.bind('change', this.onChange);
        }
        if (options.type1View) {
            this.type1View = options.type1View;
            this.type1View.bind('select', this.onChange);
        }
        if (options.type2View) {
            this.type2View = options.type2View;
            this.type2View.bind('select', this.onChange);
        }
        
        this.render();
    },
    render : function() {
        var me = this, 
            GET = {};

        // Prepare DOM
        $(this.el).empty();
        appendTmpTo('#pieTmp', {title: this.name}, this.el);

        // Filter
        if (this.versions && this.versions.getActive().length > 0) {
            GET.version = $.toJSON( this.versions.getActive() );
        }
        if (this.maps && this.maps.getActive().length > 0) {
            GET.map = $.toJSON( this.maps.getActive() );
        }
        if (this.type1View ) {
            GET.type1 = this.type1View.getValue();
        }
        if (this.type2View) {
            GET.type2 = this.type2View.getValue();
        }

        // Render the pie
        $.ajax(this.url, {
            dataType : 'json',
            data : GET,
            success : function(data) {
                var avgDiv = $('.pieChart', me.el).empty();
                var tab = $('<table></table>');

                $.each(data, function(i, val) {
                    tab.append($('<tr><td>' + val['target_type'] + '</td><td>' + parseInt(val['target_lifetime__average']) + '</td></tr>'));
                });

                avgDiv.append(tab);
                }
        });
        
    }
});

var StartlocationView = ChartView.extend({
    el: $('#content'),
    initialize : function(options) {
        _.bindAll(this);
        this.charts = [];
        
        if (options.name) {
            this.name = options.name;
        } else {
            console.error('A pie view should have a name');
        }
        if (options.url) {
            this.url = options.url;
        } else {
            console.error('A pie view should have a url');
        }
        if (options.versions) {
            this.versions = options.versions;
            this.versions.bind('change', this.onChange);
        }
        if (options.maps) {
            this.maps = options.maps;
            this.maps.bind('change', this.onChange);
        }
        
        this.render();
    },
    render : function() {
        var me = this, 
            GET = {};

        // Prepare DOM
        $(this.el).empty();
        appendTmpTo('#pieTmp', {title: this.name}, this.el);

        // Filter
        if (this.versions && this.versions.getActive().length > 0) {
            GET.version = $.toJSON( this.versions.getActive() );
        }
        if (this.maps && this.maps.getActive().length > 0) {
            GET.map = $.toJSON( this.maps.getActive() );
        }

        // Render the pie
        $.ajax(this.url, {
            dataType : 'json',
            data : GET,
            success : function(data) {
                var avgDiv = $('.pieChart', me.el).empty();
                var tab1 = $('<table></table>');
                var tab2 = $('<table></table>');

                $.each(data.type1, function(i, val) {
                    tab1.append($('<tr><td>' + val['start_location1'] + '</td><td>' + parseInt(val['start_location1__count']) + '</td></tr>'));
                });

                $.each(data.type2, function(i, val) {
                    tab2.append($('<tr><td>' + val['start_location2'] + '</td><td>' + parseInt(val['start_location2__count']) + '</td></tr>'));
                });

                avgDiv.append( $('<h3>').text('Marines') );
                avgDiv.append(tab1);
                avgDiv.append( $('<h3>').text('Aliens') );
                avgDiv.append(tab2);
            }
        });
        
    }
});

var MultiPieView = ChartView.extend({
    el: $('#content'),
    initialize : function(options) {
        _.bindAll(this);
        this.charts = [];
        
        if (options.name) {
            this.name = options.name;
        } else {
            console.error('A pie view should have a name');
        }
        if (options.url) {
            this.url = options.url;
        } else {
            console.error('A pie view should have a url');
        }
        if (options.versions) {
            this.versions = options.versions;
            this.versions.bind('change', this.onChange);
        }
        if (options.maps) {
            this.maps = options.maps;
            this.maps.bind('change', this.onChange);
        }
        if (options.type1View) {
            this.type1View = options.type1View;
            this.type1View.bind('select', this.onChange);
        }
        if (options.type2View) {
            this.type2View = options.type2View;
            this.type2View.bind('select', this.onChange);
        }
        if (options.location1View) {
            this.location1View = options.location1View;
            this.location1View.bind('select', this.onChange);
        }
        if (options.location2View) {
            this.location2View = options.location2View;
            this.location2View.bind('select', this.onChange);
        }
        
        this.render();
    },
    render : function() {
        var me = this, 
            GET = {};

        // Prepare DOM
        $(this.el).empty();
        appendTmpTo('#pieTmp', {title: this.name}, this.el);

        // Filter
        if (this.versions && this.versions.getActive().length > 0) {
            GET.version = $.toJSON( this.versions.getActive() );
        }
        if (this.maps && this.maps.getActive().length > 0) {
            GET.map = $.toJSON( this.maps.getActive() );
        }
        if (this.type1View ) {
            GET.type1 = this.type1View.getValue();
        }
        if (this.type2View) {
            GET.type2 = this.type2View.getValue();
        }
        if (this.location1View && this.location1View.getValue()) {
            GET.location1 = this.location1View.getValue();
        }
        if (this.location2View && this.location2View.getValue()) {
            GET.location2 = this.location2View.getValue();
        }

        // Render the pie
        $.ajax(this.url, {
            dataType : 'json',
            data : GET,
            success : function(response) {
                
                _(response.data).each(function(row) {
                    var data = {
                        data: [
                            [response.order[0], row[1]],
                            [response.order[1], row[2]]
                        ],
                        colors: response.colors,
                        title: row[0]
                    }
                    me.addPie(data);
                });

            }
        });
    },
    addPie: function(pieData) {
        var el = $('<div>'),
            data = new google.visualization.DataTable(),
            chart = new google.visualization.PieChart( el[0] ),
            options = {};
        
        $('.pieChart', this.el).append(el);
        
        data.addColumn('string', 'Categories');
        data.addColumn('number', 'Count');

        data.addRows(pieData.data);
        
        if (pieData.colors) {
            options.colors = pieData.colors;
        }           
        _.extend(options, PIE_OPTIONS);
        options.height = 170;
        options.width = 220;
        options.title = pieData.title;
                
        chart.draw(data, options);
        
        this.charts.push(chart);
    }
});

var DoubleBarView = ChartView.extend({
    el: $('#content'),
    initialize : function(options) {
        _.bindAll(this);
        this.charts = [];
        
        if (options.name) {
            this.name = options.name;
        } else {
            console.error('A pie view should have a name');
        }
        if (options.url) {
            this.url = options.url;
        } else {
            console.error('A pie view should have a url');
        }
        if (options.versions) {
            this.versions = options.versions;
            this.versions.bind('change', this.onChange);
        }
        if (options.maps) {
            this.maps = options.maps;
            this.maps.bind('change', this.onChange);
        }
        if (options.location1View) {
            this.location1View = options.location1View;
            this.location1View.bind('select', this.onChange);
        }
        if (options.location2View) {
            this.location2View = options.location2View;
            this.location2View.bind('select', this.onChange);
        }
        
        this.render();
    },
    render : function() {
        var me = this, 
            GET = {};

        // Prepare DOM
        $(this.el).empty();
        appendTmpTo('#pieTmp', {title: this.name}, this.el);

        // Filter
        if (this.versions && this.versions.getActive().length > 0) {
            GET.version = $.toJSON( this.versions.getActive() );
        }
        if (this.maps && this.maps.getActive().length > 0) {
            GET.map = $.toJSON( this.maps.getActive() );
        }
        if (this.location1View && this.location1View.getValue()) {
            GET.location1 = this.location1View.getValue();
        }
        if (this.location2View && this.location2View.getValue()) {
            GET.location2 = this.location2View.getValue();
        }

        // Render the pie
        $.ajax(this.url, {
            dataType : 'json',
            data : GET,
            success : function(response) {
                var data = new google.visualization.DataTable(),
                    chart = new google.visualization.BarChart( $('.pieChart', me.el)[0] ),
                    options = {};
                
                data.addColumn('string', 'Categories');
                data.addColumn('number', 'Marines');
                data.addColumn('number', 'Aliens');
                data.addRows(response.data);
                
                if (response.colors) {
                    options.colors = response.colors;
                }
                _.extend(options, BAR_OPTIONS);
                
                chart.draw(data, options);
                
                me.charts.push(chart);

                me.$el.append('<p>Average: '+ parseInt(response.average / 60) +'</p>');
            }
        });
    }
});

var AreaView = ChartView.extend({
    el: $('#content'),
    initialize : function(options) {
        _.bindAll(this);
        this.charts = [];
        
        if (options.name) {
            this.name = options.name;
        } else {
            console.error('A pie view should have a name');
        }
        if (options.url) {
            this.url = options.url;
        } else {
            console.error('A pie view should have a url');
        }
        if (options.versions) {
            this.versions = options.versions;
            this.versions.bind('change', this.onChange);
        }
        if (options.maps) {
            this.maps = options.maps;
            this.maps.bind('change', this.onChange);
        }
        
        this.render();
    },
    render : function() {
        var me = this, 
            GET = {};

        // Prepare DOM
        $(this.el).empty();
        appendTmpTo('#pieTmp', {title: this.name}, this.el);

        // Filter
        if (this.versions && this.versions.getActive().length > 0) {
            GET.version = $.toJSON( this.versions.getActive() );
        }
        if (this.maps && this.maps.getActive().length > 0) {
            GET.map = $.toJSON( this.maps.getActive() );
        }

        // Render the pie
        $.ajax(this.url, {
            dataType : 'json',
            data : GET,
            success : function(response) {
                var data = new google.visualization.DataTable(),
                    chart = new google.visualization.LineChart( $('.pieChart', me.el)[0] ),
                    options = {
                        isStacked : false,
                        height : 500,
                        colors : [
                            'red',
                            'blue', 
                            '#8888FF', 
                            '#8888FF', 
                            '#8888CC', 
                            '#8888CC', 
                            '#aaaaaa', 
                            '#aaaaaa'
                        ],
                        series : [{
                            lineWidth : 4
                        },{
                            lineWidth : 4
                        },{
                            lineWidth : 3
                        },{
                            lineWidth : 3
                        },{
                            lineWidth : 2
                        },{
                            lineWidth : 2
                        },{
                            lineWidth : 2
                        },{
                            lineWidth : 2
                        },]
                    };
                    
                
                data.addColumn('string', 'Build');
                data.addColumn('number', 'Average');
                data.addColumn('number', 'Median (50%)');
                data.addColumn('number', '1st Quartile (25%)');
                data.addColumn('number', '3rd Quartile (75%)');
                data.addColumn('number', '1st Decile (10%)');
                data.addColumn('number', '9th Decile (90%)');
                data.addColumn('number', '1st Percentile (1%)');
                data.addColumn('number', '99th Percentile (99%)');
                /*data.addRows(response.data);
                
                if (response.colors) {
                    options.colors = response.colors;
                }*/
                data.addRows(response);

                var opt = {};
                
                _.extend(opt, BAR_OPTIONS);
                _.extend(opt, options);
                
                chart.draw(data, options);
                
                me.charts.push(chart);
            }
        });
    }
});

var BarView = ChartView.extend({
    el: $('#content'),
    initialize : function(options) {
        _.bindAll(this);
        this.charts = [];
        
        if (options.name) {
            this.name = options.name;
        } else {
            console.error('A pie view should have a name');
        }
        if (options.url) {
            this.url = options.url;
        } else {
            console.error('A pie view should have a url');
        }
        if (options.versions) {
            this.versions = options.versions;
            this.versions.bind('change', this.onChange);
        }
        if (options.maps) {
            this.maps = options.maps;
            this.maps.bind('change', this.onChange);
        }
        
        this.render();
    },
    render : function() {
        var me = this, 
            GET = {};

        // Prepare DOM
        $(this.el).empty();
        appendTmpTo('#pieTmp', {title: this.name}, this.el);

        // Filter
        if (this.versions && this.versions.getActive().length > 0) {
            GET.version = $.toJSON( this.versions.getActive() );
        }
        if (this.maps && this.maps.getActive().length > 0) {
            GET.map = $.toJSON( this.maps.getActive() );
        }

        // Render the pie
        $.ajax(this.url, {
            dataType : 'json',
            data : GET,
            success : function(response) {
                var data = new google.visualization.DataTable(),
                    chart = new google.visualization.BarChart( $('.pieChart', me.el)[0] ),
                    options = {};
                
                data.addColumn('string', 'Categories');
                data.addColumn('number', 'Count');
                data.addRows(response.data);
                
                if (response.colors) {
                    options.colors = response.colors;
                }
                _.extend(options, BAR_OPTIONS);
                options.height = 1000;
                
                chart.draw(data, options);
                
                me.charts.push(chart);
            }
        });
    }
});

var ConfigButtonView = Backbone.View.extend({
    initialize: function() {
        _.bindAll(this);
        this.render();
    },
    render: function() {
        $('#config-button').button({
            icons: {
                primary: "ui-icon-gear"
            },
            text: false
        });
        $('#bbutton').button({
            text: false
        })
    }
});

var NotImplementedView = ChartView.extend({
    
    initialize: function() {
        _.bindAll(this);
        this.render();
    },
    
    render: function() {
        $(this.el).empty();
        $(this.el).append('<h2>Not Implemented</h2>');
    }
});

var WelcomeView = ChartView.extend({
    
    initialize: function() {
        _.bindAll(this);
        this.render();
    },
    
    render: function() {
        $(this.el).empty();
        $(this.el).append('<h2>Welcome</h2>');
    }
});

/* ------------------- Routing -----------------*/

StatApp = new (Backbone.Router.extend({
    routes : {
        "win" : "win", 
        "kill" : "kill",
        'cpucore': 'cpucore',
        'cpuspeed': 'cpuspeed',
        'notImplemented': 'notImplemented',
        'gpu': 'gpu',
        'lifetime': 'lifetime',
        'duel': 'duel',
        'duelweapon': 'duelweapon',
        'winlength': 'winlength',
        'winpielength': 'winpielength',
        'windistance': 'windistance',
        'winpiedistance': 'winpiedistance',
        'resolution': 'resolution',
        'performance': 'performance',
        'startlocation': 'startlocation'
    },
    
    notImplemented: function() {
        this.filterView.hide();
        this.currentView.remove();
        
        this.currentView = new NotImplementedView({
            el: $('#content')
        });
    },
    
    duelweapon : function() {
        this.filterView.show(['maps','versions','type1','type2']);
        
        this.currentView.remove();      
        this.currentView = new MultiPieView({
            el: $('#content'),
            name: 'Duel - Weapon',
            url: '/kill/weapon/pie',
            versions: this.versionCollection,
            maps: this.mapCollection,
            type1View: this.filterType1View,
            type2View: this.filterType2View
        });
    },
    
    duel : function() {
        this.filterView.show(['maps','versions','type1','type2']);
        
        this.currentView.remove();      
        this.currentView = new PieView({
            el: $('#content'),
            name: 'Duel',
            url: '/kill/pie',
            versions: this.versionCollection,
            maps: this.mapCollection,
            type1View: this.filterType1View,
            type2View: this.filterType2View
        });
    },
    
    lifetime : function() {
        this.filterView.show(['maps','versions']);
        
        this.currentView.remove();      
        this.currentView = new LifetimeView({
            el: $('#content'),
            name: 'Lifetime - Average',
            url: '/lifetime',
            versions: this.versionCollection,
            maps: this.mapCollection
        });
    },

    startlocation : function() {
        this.filterView.show(['maps','versions']);
        
        this.currentView.remove();      
        this.currentView = new StartlocationView({
            el: $('#content'),
            name: 'Start location',
            url: '/startlocationcount',
            versions: this.versionCollection,
            maps: this.mapCollection
        });
    },
    
    win : function() {
        this.filterView.show(['maps','versions','location1','location2']);
        
        this.currentView.remove();      
        this.currentView = new PieView({
            el: $('#content'),
            name: 'Win',
            url: '/win/pie',
            versions: this.versionCollection,
            maps: this.mapCollection,
            location1View: this.filterLocation1View,
            location2View: this.filterLocation2View
        });
    },
    
    kill : function() {
        this.filterView.show(['maps','versions']);
        
        this.currentView.remove();      
        this.currentView = new PieView({
            el: $('#content'),
            name: 'Kill',
            url: '/kill/pie',
            versions: this.versionCollection,
            maps: this.mapCollection
        });
    },
    
    winlength: function() {
        this.filterView.show(['maps','versions','location1','location2']);
        
        this.currentView.remove();      
        this.currentView = new DoubleBarView({
            el: $('#content'),
            name: 'Win - Game Length (Bar)',
            url: '/win/bar',
            versions: this.versionCollection,
            maps: this.mapCollection,
            location1View: this.filterLocation1View,
            location2View: this.filterLocation2View
        });
    },
    
    windistance: function() {
        this.filterView.show(['maps','versions','location1','location2']);
        
        this.currentView.remove();      
        this.currentView = new DoubleBarView({
            el: $('#content'),
            name: 'Win - Start distance (Bar)',
            url: '/win/distance',
            versions: this.versionCollection,
            maps: this.mapCollection,
            location1View: this.filterLocation1View,
            location2View: this.filterLocation2View
        });
    },
    
    resolution: function() {
        this.filterView.hide();
        
        this.currentView.remove();      
        this.currentView = new BarView({
            el: $('#content'),
            name: 'Resolution',
            url: '/resolution'
        });
    },
    
    performance: function() {
        this.filterView.hide();
        
        this.currentView.remove();      
        this.currentView = new AreaView({
            el: $('#content'),
            name: 'Performance',
            url: '/performance/graph'
        });
    },
    
    winpielength: function() {
        this.filterView.show(['maps','versions','location1','location2']);
        
        this.currentView.remove();      
        this.currentView = new MultiPieView({
            el: $('#content'),
            name: 'Win - Game Length (Pie)',
            url: '/win/bar',
            versions: this.versionCollection,
            maps: this.mapCollection,
            location1View: this.filterLocation1View,
            location2View: this.filterLocation2View
        });
    },
    
    winpiedistance: function() {
        this.filterView.show(['maps','versions','location1','location2']);
        
        this.currentView.remove();      
        this.currentView = new MultiPieView({
            el: $('#content'),
            name: 'Win - Start distance (Pie)',
            url: '/win/distance',
            versions: this.versionCollection,
            maps: this.mapCollection,
            location1View: this.filterLocation1View,
            location2View: this.filterLocation2View
        });
    },
    
    cpucore : function() {
        this.filterView.hide();
        
        this.currentView.remove();      
        this.currentView = new PieView({
            el: $('#content'),
            name: 'Number Of CPU Core',
            url: '/cpucore'
        });
    },
    
    cpuspeed : function() {
        this.filterView.hide();
        
        this.currentView.remove();      
        this.currentView = new PieView({
            el: $('#content'),
            name: 'CPU Frequency',
            url: '/cpuspeed'
        });
    },
    
    gpu : function() {
        this.filterView.hide();
        
        this.currentView.remove();      
        this.currentView = new PieView({
            el: $('#content'),
            name: 'GPU Constructor',
            url: '/gpu'
        });
    },
    
    start: function() {
        var me = this;
        
        this.versionCollection = new FilterItemCollection({
            url: 'versions'
        });
        this.versionCollection.fetch();
        
        this.mapCollection = new FilterItemCollection(configMaps);
        
        this.typeCollection = new FilterItemCollection({
            url: 'types'
        });
        this.typeCollection.fetch();
        
        this.location1Collection = new FilterItemCollection({
            url: '/location1'
        });
        this.location1Collection.fetch();
        
        this.location2Collection = new FilterItemCollection({
            url: '/location2'
        });
        this.location2Collection.fetch();

        // View
        this.filterVersionsView = new FilterCheckView({
            el: $( '#filter-versions' ),
            collection: this.versionCollection
        });
        this.filterMapsView = new FilterCheckView({
            el: $( '#filter-maps' ),
            collection: this.mapCollection
        });
        
        this.filterType1View = new FilterSelectView({
            el: $( '#filter-type-1' ),
            collection: this.typeCollection
        });
        
        this.filterType2View = new FilterSelectView({
            el: $( '#filter-type-2' ),
            collection: this.typeCollection
        });
        
        this.filterLocation1View = new FilterSelectLocationView({
            el: $( '#filter-location-1' ),
            collection: this.location1Collection,
            'maps': this.mapCollection
        });
        
        this.filterLocation2View = new FilterSelectLocationView({
            el: $( '#filter-location-2' ),
            collection: this.location2Collection,
            'maps': this.mapCollection
        });
        
        this.filterView = new FilterView({
            el: $('#filters-widget'),
            'maps': this.filterMapsView,
            'versions': this.filterVersionsView,
            'type1': this.filterType1View,
            'type2': this.filterType2View,
            'location1': this.filterLocation1View,
            'location2': this.filterLocation2View
        });     

        this.menuView = new MenuView({
            el: $('#main-menu .menu-list'),
            config : configMenu
        });

        this.configView = new ConfigButtonView({
            el: $('#config-button'),
            config : configMenu
        });
        
        this.currentView = new WelcomeView();
        
        Backbone.history.start();
    }
}));

