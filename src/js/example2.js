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
  var json = {
    "children": [
        {
            "children": [
                {
                    "children": [], 
                    "data": {
                        "description": ".git/hooks", 
                        "$color": "#b7a25c", 
                        "typec": ".sample", 
                        "sizec": 14044, 
                        "lvl": 2, 
                        "types": ".sample", 
                        "size": 14044
                    }, 
                    "id": "../.git/hooks", 
                    "name": ".git/hooks"
                }, 
                {
                    "children": [], 
                    "data": {
                        "description": ".git/info", 
                        "$color": "#05d9c1", 
                        "typec": "[none]", 
                        "sizec": 240, 
                        "lvl": 2, 
                        "types": "[none]", 
                        "size": 240
                    }, 
                    "id": "../.git/info", 
                    "name": ".git/info"
                }, 
                {
                    "children": [
                        {
                            "children": [
                                {
                                    "children": [], 
                                    "data": {
                                        "description": ".git/logs/refs/heads", 
                                        "$color": "#d6b949", 
                                        "typec": "[none]", 
                                        "sizec": 310, 
                                        "lvl": 4, 
                                        "types": "[none]", 
                                        "size": 310
                                    }, 
                                    "id": "../.git/logs/refs/heads", 
                                    "name": ".git/logs/refs/heads"
                                }, 
                                {
                                    "children": [
                                        {
                                            "children": [], 
                                            "data": {
                                                "description": ".git/logs/refs/remotes/origin", 
                                                "$color": "#06bbe9", 
                                                "typec": "[none]", 
                                                "sizec": 134, 
                                                "lvl": 5, 
                                                "types": "[none]", 
                                                "size": 134
                                            }, 
                                            "id": "../.git/logs/refs/remotes/origin", 
                                            "name": ".git/logs/refs/remotes/origin"
                                        }
                                    ], 
                                    "data": {
                                        "description": ".git/logs/refs/remotes", 
                                        "$color": "#67995d", 
                                        "typec": "NULL", 
                                        "sizec": 134, 
                                        "lvl": 4, 
                                        "types": "NULL", 
                                        "size": 0
                                    }, 
                                    "id": "../.git/logs/refs/remotes", 
                                    "name": ".git/logs/refs/remotes"
                                }
                            ], 
                            "data": {
                                "description": ".git/logs/refs", 
                                "$color": "#704bdd", 
                                "typec": "NULL", 
                                "sizec": 444, 
                                "lvl": 3, 
                                "types": "NULL", 
                                "size": 0
                            }, 
                            "id": "../.git/logs/refs", 
                            "name": ".git/logs/refs"
                        }
                    ], 
                    "data": {
                        "description": ".git/logs", 
                        "$color": "#4f790f", 
                        "typec": "[none]", 
                        "sizec": 754, 
                        "lvl": 2, 
                        "types": "[none]", 
                        "size": 310
                    }, 
                    "id": "../.git/logs", 
                    "name": ".git/logs"
                }, 
                {
                    "children": [
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/objects/06", 
                                "$color": "#1bac8d", 
                                "typec": "[none]", 
                                "sizec": 98, 
                                "lvl": 3, 
                                "types": "[none]", 
                                "size": 98
                            }, 
                            "id": "../.git/objects/06", 
                            "name": ".git/objects/06"
                        }, 
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/objects/63", 
                                "$color": "#e48f94", 
                                "typec": "[none]", 
                                "sizec": 127, 
                                "lvl": 3, 
                                "types": "[none]", 
                                "size": 127
                            }, 
                            "id": "../.git/objects/63", 
                            "name": ".git/objects/63"
                        }, 
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/objects/69", 
                                "$color": "#489909", 
                                "typec": "[none]", 
                                "sizec": 60, 
                                "lvl": 3, 
                                "types": "[none]", 
                                "size": 60
                            }, 
                            "id": "../.git/objects/69", 
                            "name": ".git/objects/69"
                        }, 
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/objects/6f", 
                                "$color": "#c5caf7", 
                                "typec": "[none]", 
                                "sizec": 162, 
                                "lvl": 3, 
                                "types": "[none]", 
                                "size": 162
                            }, 
                            "id": "../.git/objects/6f", 
                            "name": ".git/objects/6f"
                        }, 
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/objects/8d", 
                                "$color": "#9d60f3", 
                                "typec": "[none]", 
                                "sizec": 1932, 
                                "lvl": 3, 
                                "types": "[none]", 
                                "size": 1932
                            }, 
                            "id": "../.git/objects/8d", 
                            "name": ".git/objects/8d"
                        }, 
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/objects/91", 
                                "$color": "#f0ce8e", 
                                "typec": "[none]", 
                                "sizec": 78, 
                                "lvl": 3, 
                                "types": "[none]", 
                                "size": 78
                            }, 
                            "id": "../.git/objects/91", 
                            "name": ".git/objects/91"
                        }, 
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/objects/9c", 
                                "$color": "#7ae877", 
                                "typec": "[none]", 
                                "sizec": 563, 
                                "lvl": 3, 
                                "types": "[none]", 
                                "size": 563
                            }, 
                            "id": "../.git/objects/9c", 
                            "name": ".git/objects/9c"
                        }, 
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/objects/a3", 
                                "$color": "#01b021", 
                                "typec": "[none]", 
                                "sizec": 3090, 
                                "lvl": 3, 
                                "types": "[none]", 
                                "size": 3090
                            }, 
                            "id": "../.git/objects/a3", 
                            "name": ".git/objects/a3"
                        }, 
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/objects/ce", 
                                "$color": "#4d6e16", 
                                "typec": "[none]", 
                                "sizec": 134, 
                                "lvl": 3, 
                                "types": "[none]", 
                                "size": 134
                            }, 
                            "id": "../.git/objects/ce", 
                            "name": ".git/objects/ce"
                        }, 
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/objects/info", 
                                "$color": "#404109", 
                                "typec": "NULL", 
                                "sizec": 0, 
                                "lvl": 3, 
                                "types": "NULL", 
                                "size": 0
                            }, 
                            "id": "../.git/objects/info", 
                            "name": ".git/objects/info"
                        }, 
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/objects/pack", 
                                "$color": "#c817da", 
                                "typec": "NULL", 
                                "sizec": 0, 
                                "lvl": 3, 
                                "types": "NULL", 
                                "size": 0
                            }, 
                            "id": "../.git/objects/pack", 
                            "name": ".git/objects/pack"
                        }
                    ], 
                    "data": {
                        "description": ".git/objects", 
                        "$color": "#020734", 
                        "typec": "NULL", 
                        "sizec": 6244, 
                        "lvl": 2, 
                        "types": "NULL", 
                        "size": 0
                    }, 
                    "id": "../.git/objects", 
                    "name": ".git/objects"
                }, 
                {
                    "children": [
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/refs/heads", 
                                "$color": "#82f4bf", 
                                "typec": "[none]", 
                                "sizec": 41, 
                                "lvl": 3, 
                                "types": "[none]", 
                                "size": 41
                            }, 
                            "id": "../.git/refs/heads", 
                            "name": ".git/refs/heads"
                        }, 
                        {
                            "children": [
                                {
                                    "children": [], 
                                    "data": {
                                        "description": ".git/refs/remotes/origin", 
                                        "$color": "#59a4fc", 
                                        "typec": "[none]", 
                                        "sizec": 41, 
                                        "lvl": 4, 
                                        "types": "[none]", 
                                        "size": 41
                                    }, 
                                    "id": "../.git/refs/remotes/origin", 
                                    "name": ".git/refs/remotes/origin"
                                }
                            ], 
                            "data": {
                                "description": ".git/refs/remotes", 
                                "$color": "#244d58", 
                                "typec": "NULL", 
                                "sizec": 41, 
                                "lvl": 3, 
                                "types": "NULL", 
                                "size": 0
                            }, 
                            "id": "../.git/refs/remotes", 
                            "name": ".git/refs/remotes"
                        }, 
                        {
                            "children": [], 
                            "data": {
                                "description": ".git/refs/tags", 
                                "$color": "#1a4ff2", 
                                "typec": "NULL", 
                                "sizec": 0, 
                                "lvl": 3, 
                                "types": "NULL", 
                                "size": 0
                            }, 
                            "id": "../.git/refs/tags", 
                            "name": ".git/refs/tags"
                        }
                    ], 
                    "data": {
                        "description": ".git/refs", 
                        "$color": "#418a2d", 
                        "typec": "NULL", 
                        "sizec": 82, 
                        "lvl": 2, 
                        "types": "NULL", 
                        "size": 0
                    }, 
                    "id": "../.git/refs", 
                    "name": ".git/refs"
                }
            ], 
            "data": {
                "description": ".git", 
                "$color": "#e2f136", 
                "typec": "[none]", 
                "sizec": 22519, 
                "lvl": 1, 
                "types": "[none]", 
                "size": 1155
            }, 
            "id": "../.git", 
            "name": ".git"
        }, 
        {
            "children": [
                {
                    "children": [], 
                    "data": {
                        "description": "src/css", 
                        "$color": "#bf17ac", 
                        "typec": ".css", 
                        "sizec": 2448, 
                        "lvl": 2, 
                        "types": ".css", 
                        "size": 2448
                    }, 
                    "id": "../src/css", 
                    "name": "src/css"
                }
            ], 
            "data": {
                "description": "src", 
                "$color": "#245956", 
                "typec": ".json", 
                "sizec": 359645, 
                "lvl": 1, 
                "types": ".js", 
                "size": 357197
            }, 
            "id": "../src", 
            "name": "src"
        }, 
        {
            "children": [], 
            "data": {
                "description": "testdata", 
                "$color": "#be159e", 
                "typec": ".json", 
                "sizec": 3270, 
                "lvl": 1, 
                "types": ".json", 
                "size": 3270
            }, 
            "id": "../testdata", 
            "name": "testdata"
        }
    ], 
    "data": {
        "description": "", 
        "$color": "#79480b", 
        "typec": "[none]", 
        "sizec": 391582, 
        "lvl": 0, 
        "types": "[none]", 
        "size": 6148
    }, 
    "id": "../", 
    "name": ""
};

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
            'color': '#33dddd'
          },
          stylesHover: {
            'color': '#dd3333'
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
