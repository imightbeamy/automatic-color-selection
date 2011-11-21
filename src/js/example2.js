var labelType, useGradients, nativeTextSupport, animate;

(function() {
  var ua = navigator.userAgent,
      iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
      typeOfCanvas = typeof HTMLCanvasElement,
      nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
      textSupport = nativeCanvasSupport 
        && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
  //I'm setting this based on the fact that ExCanvas provides text support for IE
  //and that as of today iPhone/iPad current text support is lame
  labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
  nativeTextSupport = labelType == 'Native';
  useGradients = nativeCanvasSupport;
  animate = !(iStuff || !nativeCanvasSupport);
})();

var Log = {
  elem: false,
  write: function(text){
    if (!this.elem) 
      this.elem = document.getElementById('log');
    this.elem.innerHTML = text;
    this.elem.style.left = (500 - this.elem.offsetWidth / 2) + 'px';
  }
};


function init(){
  //init data
  var json = 
{"children": [{"children": [{"children": [], "data": {"description": "examples/filestructure", "$color": "#bfa03f", "sizec": 6148, "typec": "[none]", "$angularWidth": 6148, "lvl": 2, "types": "[none]", "size": 6148}, "id": "../examples/filestructure", "name": "examples/filestructure"}], "data": {"description": "examples", "$color": "#bfa73f", "sizec": 12296, "typec": "[none]", "$angularWidth": 6148, "lvl": 1, "types": "[none]", "size": 6148}, "id": "../examples", "name": "examples"}, {"children": [{"children": [], "data": {"description": "src/css", "$color": "#3fbf63", "sizec": 2448, "typec": ".css", "$angularWidth": 2448, "lvl": 2, "types": ".css", "size": 2448}, "id": "../src/css", "name": "src/css"}, {"children": [], "data": {"description": "src/js", "$color": "#bf3f88", "sizec": 169496, "typec": ".js", "$angularWidth": 169496, "lvl": 2, "types": ".js", "size": 169496}, "id": "../src/js", "name": "src/js"}, {"children": [], "data": {"description": "src/python", "$color": "#3fbf63", "sizec": 38048, "typec": ".py", "$angularWidth": 38048, "lvl": 2, "types": ".pyc", "size": 38048}, "id": "../src/python", "name": "src/python"}], "data": {"description": "src", "$color": "#bf3f62", "sizec": 221527, "typec": ".json", "$angularWidth": 11535, "lvl": 1, "types": "[none]", "size": 11535}, "id": "../src", "name": "src"}, {"children": [{"children": [], "data": {"description": "testdata/filestructure", "$color": "#bfb43f", "sizec": 48109, "typec": ".json", "$angularWidth": 48109, "lvl": 2, "types": ".json", "size": 48109}, "id": "../testdata/filestructure", "name": "testdata/filestructure"}], "data": {"description": "testdata", "$color": "#59bf3f", "sizec": 48109, "typec": "NULL", "$angularWidth": 0, "lvl": 1, "types": "NULL", "size": 0}, "id": "../testdata", "name": "testdata"}], "data": {"description": "", "$color": "#3fadbf", "sizec": 396808, "typec": "[none]", "$angularWidth": 6240, "lvl": 0, "types": "[none]", "size": 6240}, "id": "../", "name": "root"}
;

    //end
    //init Sunburst
    var sb = new $jit.Sunburst({
        //id container for the visualization
        injectInto: 'infovis',
        //Distance between levels
        levelDistance: 90,
        //Change node and edge styles such as
        //color, width and dimensions.
        Node: {
          overridable: true,
          type: useGradients? 'gradient-multipie' : 'multipie'
        },
        //Select canvas labels
        //'HTML', 'SVG' and 'Native' are possible options
        Label: {
          type: labelType
        },
        //Change styles when hovering and clicking nodes
        NodeStyles: {
          enable: true,
          type: 'Native',
          stylesClick: {
            'alpha': .4
          },
          stylesHover: {
            'alpha': .8
          }
        },
        //Add tooltips
        Tips: {
          enable: true,
          onShow: function(tip, node) {
            var html = "<div class=\"tip-title\">" + node.name + "</div>"; 
            var data = node.data;
            if("days" in data) {
              html += "<b>Last modified:</b> " + data.days + " days ago";
            }
            if("size" in data) {
              html += "<br /><b>File size:</b> " + Math.round(data.size / 1024) + "KB";
            }
            tip.innerHTML = html;
          }
        },
        //implement event handlers
        Events: {
          enable: true,
          onClick: function(node) {
            if(!node) return;
            //Build detailed information about the file/folder
            //and place it in the right column.
            var html = "<h4>" + node.name + "</h4>", data = node.data;
            if("days" in data) {
              html += "<b>Last modified:</b> " + data.days + " days ago";
            }
            if("size" in data) {
              html += "<br /><br /><b>File size:</b> " + Math.round(data.size / 1024) + "KB";
            }
            if("description" in data) {
              html += "<br /><br /><b>Last commit was:</b><br /><pre>" + data.description + "</pre>";
            }
            $jit.id('inner-details').innerHTML = html;
            //hide tip
            sb.tips.hide();
            //rotate
            sb.rotate(node, animate? 'animate' : 'replot', {
              duration: 1000,
              transition: $jit.Trans.Quart.easeInOut
            });
          }
        },
        // Only used when Label type is 'HTML' or 'SVG'
        // Add text to the labels. 
        // This method is only triggered on label creation
        onCreateLabel: function(domElement, node){
          var labels = sb.config.Label.type,
              aw = node.getData('angularWidth');
          if (labels === 'HTML' && (node._depth < 2 || aw > 2000)) {
            domElement.innerHTML = node.name;
          } else if (labels === 'SVG' && (node._depth < 2 || aw > 2000)) {
            domElement.firstChild.appendChild(document.createTextNode(node.name));
          }
        },
        // Only used when Label type is 'HTML' or 'SVG'
        // Change node styles when labels are placed
        // or moved.
        onPlaceLabel: function(domElement, node){
          var labels = sb.config.Label.type;
          if (labels === 'SVG') {
            var fch = domElement.firstChild;
            var style = fch.style;
            style.display = '';
            style.cursor = 'pointer';
            style.fontSize = "0.8em";
            fch.setAttribute('fill', "#fff");
          } else if (labels === 'HTML') {
            var style = domElement.style;
            style.display = '';
            style.cursor = 'pointer';
            style.fontSize = "0.8em";
            style.color = "#ddd";
            var left = parseInt(style.left);
            var w = domElement.offsetWidth;
            style.left = (left - w / 2) + 'px';
          }
        }
   });
    //load JSON data.
    sb.loadJSON(json);
    //compute positions and plot.
    sb.refresh();
    //end
}
