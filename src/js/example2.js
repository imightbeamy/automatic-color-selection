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
{"children": [{"children": [{"children": [], "data": {"description": "examples/filestructure", "$color": "#6fbf3f", "sizec": 596642, "typec": ".png", "$angularWidth": 596642, "lvl": 2, "types": ".png", "size": 596642}, "id": "../../examples/filestructure", "name": "examples/filestructure"}, {"children": [], "data": {"description": "examples/otherexam", "$color": "#bfb13f", "sizec": 6148, "typec": "[none]", "$angularWidth": 6148, "lvl": 2, "types": "[none]", "size": 6148}, "id": "../../examples/otherexam", "name": "examples/otherexam"}], "data": {"description": "examples", "$color": "#8c3fbf", "sizec": 608938, "typec": "[none]", "$angularWidth": 6148, "lvl": 1, "types": "[none]", "size": 6148}, "id": "../../examples", "name": "examples"}, {"children": [{"children": [], "data": {"description": "src/css", "$color": "#3f50bf", "sizec": 15002, "typec": ".css", "$angularWidth": 15002, "lvl": 2, "types": ".png", "size": 15002}, "id": "../../src/css", "name": "src/css"}, {"children": [], "data": {"description": "src/Icicle_files", "$color": "#3fa4bf", "sizec": 170581, "typec": ".js", "$angularWidth": 170581, "lvl": 2, "types": ".js", "size": 170581}, "id": "../../src/Icicle_files", "name": "src/Icicle_files"}, {"children": [], "data": {"description": "src/js", "$color": "#3fbf64", "sizec": 375720, "typec": ".js", "$angularWidth": 375720, "lvl": 2, "types": ".js", "size": 375720}, "id": "../../src/js", "name": "src/js"}, {"children": [], "data": {"description": "src/python", "$color": "#63bf3f", "sizec": 126010, "typec": ".py", "$angularWidth": 126010, "lvl": 2, "types": ".swp", "size": 126010}, "id": "../../src/python", "name": "src/python"}], "data": {"description": "src", "$color": "#3f5cbf", "sizec": 712995, "typec": ".html", "$angularWidth": 25682, "lvl": 1, "types": ".js", "size": 25682}, "id": "../../src", "name": "src"}, {"children": [{"children": [], "data": {"description": "testdata/filestructure", "$color": "#3fbf9a", "sizec": 54257, "typec": ".json", "$angularWidth": 54257, "lvl": 2, "types": ".json", "size": 54257}, "id": "../../testdata/filestructure", "name": "testdata/filestructure"}, {"children": [], "data": {"description": "testdata/numtwo", "$color": "#3fbfa3", "sizec": 48109, "typec": ".json", "$angularWidth": 48109, "lvl": 2, "types": ".json", "size": 48109}, "id": "../../testdata/numtwo", "name": "testdata/numtwo"}], "data": {"description": "testdata", "$color": "#903fbf", "sizec": 108514, "typec": "[none]", "$angularWidth": 6148, "lvl": 1, "types": "[none]", "size": 6148}, "id": "../../testdata", "name": "testdata"}], "data": {"description": "", "$color": "#bfae3f", "sizec": 1635507, "typec": "[none]", "$angularWidth": 12384, "lvl": 0, "types": "[none]", "size": 12384}, "id": "../../", "name": "root"}
  
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
