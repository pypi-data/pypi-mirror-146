(self["webpackChunkjupyter_scatter"] = self["webpackChunkjupyter_scatter"] || []).push([["src_index_js-webpack_sharing_consume_default_pub-sub-es_pub-sub-es-webpack_sharing_consume_de-e2b1d4"],{

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse("{\"name\":\"jupyter-scatter\",\"version\":\"0.2.2\",\"description\":\"A scatter plot extension for Jupyter Notebook and Lab\",\"author\":\"Fritz Lekschas\",\"main\":\"src/index.js\",\"repository\":{\"type\":\"git\",\"url\":\"https://github.com/flekschas/jupyter-scatter.git\"},\"license\":\"Apache-2.0\",\"keywords\":[\"scatter\",\"scatter plot\",\"jupyter\",\"jupyterlab\",\"jupyterlab-extension\"],\"files\":[\"embed.js\",\"extension.js\",\"index.js\",\"labplugin.js\",\"src/**/*.js\",\"dist/*.js\"],\"scripts\":{\"clean\":\"rimraf dist/ && rimraf ../jscatter/labextension/ && rimraf ../jscatter/nbextension\",\"prepare\":\"npm run clean && npm run build:prod\",\"build\":\"webpack --mode=development && npm run build:labextension:dev\",\"build:prod\":\"webpack --mode=production && npm run build:labextension\",\"build:labextension\":\"jupyter labextension build .\",\"build:labextension:dev\":\"jupyter labextension build --development True .\",\"watch\":\"webpack --watch --mode=development\",\"test\":\"echo \\\"Error: no test specified\\\" && exit 1\"},\"dependencies\":{\"@jupyter-widgets/base\":\"^1.1.10 || ^2 || ^3 || ^4\",\"camera-2d-simple\":\"~2.2.1\",\"dom-2d-camera\":\"~1.2.3\",\"gl-matrix\":\"^3.1.0\",\"lodash\":\"^4.17.4\",\"pub-sub-es\":\"~2.0.1\",\"regl\":\"~2.1.0\",\"regl-scatterplot\":\"^1.0.0\"},\"devDependencies\":{\"@jupyterlab/builder\":\"^3.0.8\",\"css-loader\":\"^3.5.3\",\"eslint\":\"^7.4.0\",\"eslint-config-prettier\":\"^6.11.0\",\"eslint-plugin-prettier\":\"^3.1.4\",\"lint-staged\":\"^10.2.7\",\"prettier\":\"^2.0.5\",\"pretty-quick\":\"^2.0.1\",\"rimraf\":\"^3.0.2\",\"style-loader\":\"^1.2.1\",\"webpack\":\"^5.18.0\",\"webpack-cli\":\"^4.4.0\"},\"jupyterlab\":{\"extension\":\"labplugin\",\"outputDir\":\"../jscatter/labextension\",\"sharedPackages\":{\"@jupyter-widgets/base\":{\"bundled\":false,\"singleton\":true}}}}");

/***/ }),

/***/ "./src/codecs.js":
/*!***********************!*\
  !*** ./src/codecs.js ***!
  \***********************/
/***/ ((module) => {

const DTYPES = {
  uint8: Uint8Array,
  int8: Int8Array,
  uint16: Uint16Array,
  int16: Int16Array,
  uint32: Uint32Array,
  int32: Int32Array,
  float32: Float32Array,
  float64: Float64Array,
};

class NumpyCodec {
  /** @param {keyof typeof DTYPES} dtype */
  constructor(dtype) {
    if (!(dtype in DTYPES)) {
      throw Error(`Dtype not supported, got ${JSON.stringify(dtype)}.`);
    }
    this.dtype = dtype;
  }
}

class Numpy2D extends NumpyCodec {

  /**
   * @param {{buffer: DataView, dtype: keyof typeof DTYPES, shape: [number, number]}} data
   * @returns {number[][]}
   */
  deserialize(data) {
    if (data == null) return null;
    // Take full view of data buffer
    const arr = new DTYPES[this.dtype](data.buffer.buffer);
    // Chunk single TypedArray into nested Array of points
    const [height, width] = data.shape;
    // Float32Array(width * height) -> [Array(width), Array(width), ...]
    const points = Array
      .from({ length: height })
      .map((_, i) => Array.from(arr.subarray(i * width, (i + 1) * width)));
    return points;
  }

  /**
   * @param {number[][]} data
   * @returns {{data: ArrayBuffer, dtype: keyof typeof DTYPES, shape: [number, number]}}
   */
  serialize(data) {
    const height = data.length;
    const width = data[0].length;
    const arr = new DTYPES[this.dtype](height * width);
    for (let i = 0; i < data.length; i++) {
      arr.set(data[i], i * height);
    }
    return { data: arr.buffer, dtype: this.dtype, shape: [height, width] };
  }
}

class Numpy1D extends NumpyCodec {

  /**
   * @param {{buffer: DataView, dtype: keyof typeof DTYPES, shape: [number]}} data
   * @returns {number[]}
   */
  deserialize(data) {
    if (data == null) return null;
    // for some reason can't be a typed array
    return Array.from(new DTYPES[this.dtype](data.buffer.buffer));
  }

  /**
   * @param {number[]} data
   * @returns {{data: ArrayBuffer, dtype: keyof typeof DTYPES, shape: [number]}}
   */
  serialize(data) {
    const arr = new DTYPES[this.dtype](data)
    return { data: arr.buffer, dtype: this.dtype, shape: [data.length] };
  }
}

module.exports = { Numpy1D, Numpy2D };


/***/ }),

/***/ "./src/index.js":
/*!**********************!*\
  !*** ./src/index.js ***!
  \**********************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

/* eslint-env browser */
const widgets = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const reglScatterplot = __webpack_require__(/*! regl-scatterplot/dist/regl-scatterplot.js */ "./node_modules/regl-scatterplot/dist/regl-scatterplot.js");
const codecs = __webpack_require__(/*! ./codecs */ "./src/codecs.js");
const packageJson = __webpack_require__(/*! ../package.json */ "./package.json");

const createScatterplot = reglScatterplot.default;

const JupyterScatterModel = widgets.DOMWidgetModel.extend(
  {
    defaults: {
      ...widgets.DOMWidgetModel.prototype.defaults(),
      _model_name : 'JupyterScatterModel',
      _model_module : packageJson.name,
      _model_module_version : packageJson.version,
      _view_name : 'JupyterScatterView',
      _view_module : packageJson.name,
      _view_module_version : packageJson.version
    }
  },
  {
    serializers: {
      ...widgets.DOMWidgetModel.serializers,
      points: new codecs.Numpy2D('float32'),
      selection: new codecs.Numpy1D('uint32'),
    }
  },
);

function camelToSnake(string) {
  return string.replace(/[\w]([A-Z])/g, function(m) {
    return m[0] + "_" + m[1];
  }).toLowerCase();
}

function flipObj(obj) {
  return Object.entries(obj).reduce((ret, entry) => {
    const [ key, value ] = entry;
    ret[ value ] = key;
    return ret;
  }, {});
}

function downloadBlob(blob, name) {
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = name || 'jscatter.png';

  document.body.appendChild(link);

  link.dispatchEvent(
    new MouseEvent('click', {
      bubbles: true,
      cancelable: true,
      view: window,
    })
  );

  document.body.removeChild(link);
}

const MIN_WIDTH = 240;

const properties = {
  backgroundColor: 'backgroundColor',
  backgroundImage: 'backgroundImage',
  cameraDistance: 'cameraDistance',
  cameraRotation: 'cameraRotation',
  cameraTarget: 'cameraTarget',
  cameraView: 'cameraView',
  color: 'pointColor',
  colorActive: 'pointColorActive',
  colorBy: 'colorBy',
  colorHover: 'pointColorHover',
  height: 'height',
  lassoColor: 'lassoColor',
  lassoInitiator: 'lassoInitiator',
  lassoMinDelay: 'lassoMinDelay',
  lassoMinDist: 'lassoMinDist',
  mouseMode: 'mouseMode',
  opacity: 'opacity',
  opacityBy: 'opacityBy',
  otherOptions: 'otherOptions',
  points: 'points',
  reticle: 'showReticle',
  reticleColor: 'reticleColor',
  selection: 'selectedPoints',
  size: 'pointSize',
  sizeBy: 'sizeBy',
  connect: 'showPointConnections',
  connectionColor: 'pointConnectionColor',
  connectionColorActive: 'pointConnectionColorActive',
  connectionColorHover: 'pointConnectionColorHover',
  connectionColorBy: 'pointConnectionColorBy',
  connectionOpacity: 'pointConnectionOpacity',
  connectionOpacityBy: 'pointConnectionOpacityBy',
  connectionSize: 'pointConnectionSize',
  connectionSizeBy: 'pointConnectionSizeBy',
  viewDownload: 'viewDownload',
  viewReset: 'viewReset',
  hovering: 'hovering',
};

// Custom View. Renders the widget model.
const JupyterScatterView = widgets.DOMWidgetView.extend({
  render: function render() {
    var self = this;

    Object.keys(properties).forEach(function(propertyName) {
      self[propertyName] = self.model.get(camelToSnake(propertyName));
    });

    this.height = this.model.get('height');
    this.width = !Number.isNaN(+this.model.get('width')) && +this.model.get('width') > 0
      ? +this.model.get('width')
      : 'auto';

    // Create a random 6-letter string
    // From https://gist.github.com/6174/6062387
    var randomStr = (
      Math.random().toString(36).substring(2, 5) +
      Math.random().toString(36).substring(2, 5)
    );
    this.model.set('dom_element_id', randomStr);

    this.container = document.createElement('div');
    this.container.setAttribute('id', randomStr);
    this.container.style.position = 'relative'
    this.container.style.width = this.width === 'auto'
      ? '100%'
      : this.width + 'px';
    this.container.style.height = this.height + 'px';

    this.el.appendChild(this.container);

    this.canvas = document.createElement('canvas');
    this.canvas.style.width = '100%';
    this.canvas.style.height = '100%';

    this.container.appendChild(this.canvas);

    window.requestAnimationFrame(function init() {
      const initialOptions = {
        canvas: self.canvas,
      }

      if (self.width !== 'auto') initialOptions.width = self.width;

      Object.entries(properties).forEach(function(property) {
        const pyName = property[0];
        const jsName = property[1];
        if (self[pyName] !== null)
          initialOptions[jsName] = self[pyName];
      });

      self.scatterplot = createScatterplot(initialOptions);

      // eslint-disable-next-line
      console.log(
        'jscatter v' + packageJson.version +
        ' with regl-scatterplot v' + self.scatterplot.get('version')
      );

      self.container.api = self.scatterplot;

      // Listen to events from the JavaScript world
      self.pointoverHandlerBound = self.pointoverHandler.bind(self);
      self.pointoutHandlerBound = self.pointoutHandler.bind(self);
      self.selectHandlerBound = self.selectHandler.bind(self);
      self.deselectHandlerBound = self.deselectHandler.bind(self);
      self.scatterplot.subscribe('pointover', self.pointoverHandlerBound);
      self.scatterplot.subscribe('pointout', self.pointoutHandlerBound);
      self.scatterplot.subscribe('select', self.selectHandlerBound);
      self.scatterplot.subscribe('deselect', self.deselectHandlerBound);

      // Listen to messages from the Python world
      Object.keys(properties).forEach(function(propertyName) {
        if (self[propertyName + 'Handler']) {
          self.model.on(
            'change:' + camelToSnake(propertyName),
            self.withModelChangeHandler(
              propertyName,
              self[propertyName + 'Handler'].bind(self)
            ),
            self
          );
        } else {
          console.warn('No handler for ' + propertyName);
        }
      });

      window.addEventListener('resize', self.resizeHandler.bind(self));
      window.addEventListener('deviceorientation', self.resizeHandler.bind(self));

      self.resizeHandler();
      self.colorCanvas();

      if (self.points.length) {
        self.scatterplot
          .draw(self.points)
          .then(function onInitialDraw() {
            if (self.selection.length) {
              self.scatterplot.select(self.selection, { preventEvent: true });
            }
          });
      }
    });

    this.model.save_changes();
  },

  remove: function destroy() {
    this.scatterplot.destroy();
  },

  // Helper
  colorCanvas: function colorCanvas() {
    if (Array.isArray(this.backgroundColor)) {
      this.canvas.style.backgroundColor = 'rgb(' +
        this.backgroundColor.slice(0, 3).map(function (x) { return x * 255 }).join(',') +
        ')';
    } else {
      this.canvas.style.backgroundColor = this.backgroundColor;
    }
  },

  // Event handlers for JS-triggered events
  pointoverHandler: function pointoverHandler(pointIndex) {
    this.hoveringChangedByJs = true;
    this.model.set('hovering', pointIndex);
    this.model.save_changes();
  },

  pointoutHandler: function pointoutHandler() {
    this.hoveringChangedByJs = true;
    this.model.set('hovering', null);
    this.model.save_changes();
  },

  selectHandler: function selectHandler(event) {
    this.selectionChangedByJs = true;
    this.model.set('selection', [...event.points]);
    this.model.save_changes();
  },

  deselectHandler: function deselectHandler() {
    this.selectionChangedByJs = true;
    this.model.set('selection', []);
    this.model.save_changes();
  },

  // Event handlers for Python-triggered events
  pointsHandler: function pointsHandler(newPoints) {
    this.scatterplot.draw(newPoints, {
      transition: true,
      transitionDuration: 3000,
      transitionEasing: 'quadInOut',
    });
  },

  selectionHandler: function selectionHandler(newSelection) {
    // Avoid calling `this.scatterplot.select()` twice when the selection was
    // triggered by the JavaScript (i.e., the user interactively selected points)
    if (this.selectionChangedByJs) {
      this.selectionChangedByJs = undefined;
      return;
    }

    if (!newSelection || !newSelection.length) {
      this.scatterplot.deselect({ preventEvent: true });
    } else {
      this.scatterplot.select(newSelection, { preventEvent: true });
    }
  },

  hoveringHandler: function hoveringHandler(newHovering) {
    // Avoid calling `this.scatterplot.hover()` twice when the hovering was
    // triggered by the JavaScript (i.e., the user interactively selected points)
    if (this.hoveringChangedByJs) {
      this.hoveringChangedByJs = undefined;
      return;
    }

    if (Number.isNaN(+newHovering)) {
      this.scatterplot.hover({ preventEvent: true });
    } else {
      this.scatterplot.hover(+newHovering, { preventEvent: true });
    }
  },

  heightHandler: function heightHandler(newValue) {
    this.withPropertyChangeHandler('height', newValue);
    this.resizeHandler();
  },

  backgroundColorHandler: function backgroundColorHandler(newValue) {
    this.withPropertyChangeHandler('backgroundColor', newValue);
    this.colorCanvas();
  },

  backgroundImageHandler: function backgroundImageHandler(newValue) {
    this.withPropertyChangeHandler('backgroundImage', newValue);
  },

  lassoColorHandler: function lassoColorHandler(newValue) {
    this.withPropertyChangeHandler('lassoColor', newValue);
  },

  lassoMinDelayHandler: function lassoMinDelayHandler(newValue) {
    this.withPropertyChangeHandler('lassoMinDelay', newValue);
  },

  lassoMinDistHandler: function lassoMinDistHandler(newValue) {
    this.withPropertyChangeHandler('lassoMinDist', newValue);
  },

  colorHandler: function colorHandler(newValue) {
    this.withPropertyChangeHandler('pointColor', newValue);
  },

  colorActiveHandler: function colorActiveHandler(newValue) {
    this.withPropertyChangeHandler('pointColorActive', newValue);
  },

  colorHoverHandler: function colorHoverHandler(newValue) {
    this.withPropertyChangeHandler('pointColorHover', newValue);
  },

  colorByHandler: function colorByHandler(newValue) {
    this.withPropertyChangeHandler('colorBy', newValue);
  },

  opacityHandler: function opacityHandler(newValue) {
    this.withPropertyChangeHandler('opacity', newValue);
  },

  opacityByHandler: function opacityByHandler(newValue) {
    this.withPropertyChangeHandler('opacityBy', newValue);
  },

  sizeHandler: function sizeHandler(newValue) {
    this.withPropertyChangeHandler('pointSize', newValue);
  },

  sizeByHandler: function sizeByHandler(newValue) {
    this.withPropertyChangeHandler('sizeBy', newValue);
  },

  connectHandler: function connectHandler(newValue) {
    this.withPropertyChangeHandler('showPointConnections', Boolean(newValue));
  },

  connectionColorHandler: function connectionColorHandler(newValue) {
    this.withPropertyChangeHandler('pointConnectionColor', newValue);
  },

  connectionColorActiveHandler: function connectionColorActiveHandler(newValue) {
    this.withPropertyChangeHandler('pointConnectionColorActive', newValue);
  },

  connectionColorHoverHandler: function connectionColorHoverHandler(newValue) {
    this.withPropertyChangeHandler('pointConnectionColorHover', newValue);
  },

  connectionColorByHandler: function connectionColorByHandler(newValue) {
    this.withPropertyChangeHandler('pointConnectionColorBy', newValue);
  },

  connectionOpacityHandler: function connectionOpacityHandler(newValue) {
    this.withPropertyChangeHandler('pointConnectionOpacity', newValue);
  },

  connectionOpacityByHandler: function connectionOpacityByHandler(newValue) {
    this.withPropertyChangeHandler('pointConnectionOpacityBy', newValue);
  },

  connectionSizeHandler: function connectionSizeHandler(newValue) {
    this.withPropertyChangeHandler('pointConnectionSize', newValue);
  },

  connectionSizeByHandler: function connectionSizeByHandler(newValue) {
    this.withPropertyChangeHandler('pointConnectionSizeBy', newValue);
  },

  reticleHandler: function reticleHandler(newValue) {
    this.withPropertyChangeHandler('showReticle', newValue);
  },

  reticleColorHandler: function reticleColorHandler(newValue) {
    this.withPropertyChangeHandler('reticleColor', newValue);
  },

  cameraTargetHandler: function cameraTargetHandler(newValue) {
    this.withPropertyChangeHandler('cameraTarget', newValue);
  },

  cameraDistanceHandler: function cameraDistanceHandler(newValue) {
    this.withPropertyChangeHandler('cameraDistance', newValue);
  },

  cameraRotationHandler: function cameraRotationHandler(newValue) {
    this.withPropertyChangeHandler('cameraRotation', newValue);
  },

  cameraViewHandler: function cameraViewHandler(newValue) {
    this.withPropertyChangeHandler('cameraView', newValue);
  },

  lassoInitiatorHandler: function lassoInitiatorHandler(newValue) {
    this.withPropertyChangeHandler('lassoInitiator', newValue);
  },

  mouseModeHandler: function mouseModeHandler(newValue) {
    this.withPropertyChangeHandler('mouseMode', newValue);
  },

  otherOptionsHandler: function otherOptionsHandler(newOptions) {
    this.scatterplot.set(newOptions);
  },

  viewDownloadHandler: function viewDownloadHandler(target) {
    if (!target) return;

    const data = this.scatterplot.export();

    if (target === 'property') {
      this.model.set('view_pixels', Array.from(data.pixels));
      this.model.set('view_shape', [data.width, data.height]);
      this.model.set('view_download', null);
      this.model.save_changes();
      return;
    }

    const c = document.createElement('canvas');
    c.width = data.width;
    c.height = data.height;

    const ctx = c.getContext('2d');
    ctx.putImageData(new ImageData(data.pixels, data.width, data.height), 0, 0);

    // The following is only needed to flip the image vertically. Since `ctx.scale`
    // only affects `draw*()` calls and not `put*()` calls we have to draw the
    // image twice...
    const imageObject = new Image();
    imageObject.onload = () => {
      ctx.clearRect(0, 0, data.width, data.height);
      ctx.scale(1, -1);
      ctx.drawImage(imageObject, 0, -data.height);
      c.toBlob((blob) => {
        downloadBlob(blob, 'scatter.png');
        setTimeout(() => {
          this.model.set('view_download', null);
          this.model.save_changes();
        }, 0);
      });
    };
    imageObject.src = c.toDataURL();
  },

  viewResetHandler: function viewResetHandler() {
    this.scatterplot.reset();
    setTimeout(() => {
      this.model.set('view_reset', false);
      this.model.save_changes();
    }, 0);
  },

  resizeHandler: function resizeHandler() {
    this.width = Math.max(MIN_WIDTH, this.el.getBoundingClientRect().width);
    this.container.style.height = this.height + 'px';
    this.scatterplot.set({
      width: this.width,
      height: this.height
    });
  },

  withPropertyChangeHandler: function withPropertyChangeHandler(property, changedValue) {
    var p = {};
    p[property] = changedValue;
    this.scatterplot.set(p);
  },

  withModelChangeHandler: function withModelChangeHandler(property, handler) {
    var self = this;

    return function modelChangeHandler() {
      var changes = self.model.changedAttributes();
      var pyPropertyName = camelToSnake(property);

      if (
        changes[pyPropertyName] === undefined ||
        self[property + 'Changed'] === true
      ) {
        self[property + 'Changed'] = false;
        return;
      };

      self[property] = changes[camelToSnake(property)];

      if (handler) handler(self[property]);
    }
  }
});

module.exports = {
  JupyterScatterModel: JupyterScatterModel,
  JupyterScatterView: JupyterScatterView
};


/***/ })

}]);
//# sourceMappingURL=src_index_js-webpack_sharing_consume_default_pub-sub-es_pub-sub-es-webpack_sharing_consume_de-e2b1d4.cb4a775b3d220a95e4ea.js.map