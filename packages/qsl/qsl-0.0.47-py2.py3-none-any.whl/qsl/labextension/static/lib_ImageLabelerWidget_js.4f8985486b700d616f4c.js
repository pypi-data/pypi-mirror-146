"use strict";
(self["webpackChunkqslwidgets"] = self["webpackChunkqslwidgets"] || []).push([["lib_ImageLabelerWidget_js"],{

/***/ "./lib/ImageLabelerWidget.js":
/*!***********************************!*\
  !*** ./lib/ImageLabelerWidget.js ***!
  \***********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ImageLabelerView = exports.ImageLabelerModel = void 0;
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_dom_1 = __importDefault(__webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom"));
const coreutils_1 = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const react_image_labeler_1 = __webpack_require__(/*! react-image-labeler */ "webpack/sharing/consume/default/react-image-labeler/react-image-labeler");
const hooks_1 = __webpack_require__(/*! ./hooks */ "./lib/hooks.js");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const DEFAULT_PROPERTIES = {
    type: "image",
    url: "",
    config: { image: [], regions: [] },
    labels: { image: {}, polygons: [], masks: [], boxes: [] },
    updated: Date.now(),
    action: "",
    metadata: {},
    preload: [],
    showNavigation: true,
    maxCanvasSize: 512,
    buttons: {
        next: true,
        prev: true,
        save: true,
        config: true,
        delete: true,
        ignore: true,
        unignore: true,
    },
    base: {
        serverRoot: "",
        url: "",
    },
    progress: -1,
    mode: "light",
};
const Widget = ({ model }) => {
    // @ts-ignore
    const [config, setConfig] = hooks_1.useModelState("config", model);
    // @ts-ignore
    const [url, setUrl] = hooks_1.useModelState("url", model);
    // @ts-ignore
    const [labels, setLabels] = hooks_1.useModelState("labels", model);
    // @ts-ignore
    const [updated, setUpdated] = hooks_1.useModelState("updated", model);
    // @ts-ignore
    const [action, setAction] = hooks_1.useModelState("action", model);
    // @ts-ignore
    const [type, setType] = hooks_1.useModelState("type", model);
    // @ts-ignore
    const [base, setBase] = hooks_1.useModelState("base", model);
    // @ts-ignore
    const [progress, setProgress] = hooks_1.useModelState("progress", model);
    // @ts-ignore
    const [mode, setMode] = hooks_1.useModelState("mode", model);
    // @ts-ignore
    const [buttons, setButtons] = hooks_1.useModelState("buttons", model);
    // @ts-ignore
    const [metadata, setMetadata] = hooks_1.useModelState("metadata", model);
    // @ts-ignore
    const [preload, setPreload] = hooks_1.useModelState("preload", model);
    // @ts-ignore
    const [maxCanvasSize, setMaxCanvasSize] = hooks_1.useModelState("maxCanvasSize", model);
    // @ts-ignore
    const [showNavigation, setShowNavigation] = hooks_1.useModelState("showNavigation", model);
    react_1.default.useEffect(() => {
        setBase({
            serverRoot: coreutils_1.PageConfig.getOption("serverRoot"),
            url: coreutils_1.PageConfig.getBaseUrl(),
        });
    });
    const props = {
        src: url,
        config,
        metadata,
        callbacks: {
            onSave: buttons["save"]
                ? (labels) => {
                    setLabels(labels);
                    setUpdated(Date.now());
                }
                : undefined,
            onSaveConfig: buttons["config"] ? setConfig : undefined,
            onNext: buttons["next"] ? () => setAction("next") : undefined,
            onPrev: buttons["prev"] ? () => setAction("prev") : undefined,
            onDelete: buttons["delete"] ? () => setAction("delete") : undefined,
            onIgnore: buttons["ignore"] ? () => setAction("ignore") : undefined,
            onUnignore: buttons["unignore"] ? () => setAction("unignore") : undefined,
        },
        preload,
        options: { progress, mode, maxCanvasSize, showNavigation },
    };
    return (react_1.default.createElement("div", { style: {
            padding: 16,
            backgroundColor: mode == "dark" ? "rgb(18, 18, 18)" : "white",
        } }, type == "image" ? (react_1.default.createElement(react_image_labeler_1.ImageLabeler, Object.assign({ labels: (labels || {}) }, props))) : (react_1.default.createElement(react_image_labeler_1.VideoLabeler, Object.assign({ labels: (Array.isArray(labels) ? labels : []) }, props)))));
};
class ImageLabelerModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign(Object.assign({}, super.defaults()), { _model_name: ImageLabelerModel.model_name, _model_module: ImageLabelerModel.model_module, _model_module_version: ImageLabelerModel.model_module_version, _view_name: ImageLabelerModel.view_name, _view_module: ImageLabelerModel.view_module, _view_module_version: ImageLabelerModel.view_module_version }), DEFAULT_PROPERTIES);
    }
}
exports.ImageLabelerModel = ImageLabelerModel;
ImageLabelerModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
ImageLabelerModel.model_name = "ImageLabelerModel";
ImageLabelerModel.model_module = version_1.MODULE_NAME;
ImageLabelerModel.model_module_version = version_1.MODULE_VERSION;
ImageLabelerModel.view_name = "ImageLabelerView"; // Set to null if no view
ImageLabelerModel.view_module = version_1.MODULE_NAME; // Set to null if no view
ImageLabelerModel.view_module_version = version_1.MODULE_VERSION;
class ImageLabelerView extends base_1.DOMWidgetView {
    render() {
        this.el.classList.add("qsl-image-labeler-widget");
        const component = react_1.default.createElement(Widget, {
            model: this.model,
        });
        react_dom_1.default.render(component, this.el);
    }
}
exports.ImageLabelerView = ImageLabelerView;
//# sourceMappingURL=ImageLabelerWidget.js.map

/***/ }),

/***/ "./lib/hooks.js":
/*!**********************!*\
  !*** ./lib/hooks.js ***!
  \**********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.useModelEvent = exports.useModelState = void 0;
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
/**
 *
 * @param name property name in the Python model object.
 * @returns model state and set state function.
 */
const useModelState = (name, model) => {
    const [state, setState] = react_1.default.useState(model === null || model === void 0 ? void 0 : model.get(name));
    useModelEvent(model, `change:${name}`, (model) => {
        setState(model.get(name));
    }, [name]);
    function updateModel(val, options) {
        model === null || model === void 0 ? void 0 : model.set(name, val, options);
        model === null || model === void 0 ? void 0 : model.save_changes();
    }
    return [state, updateModel];
};
exports.useModelState = useModelState;
/**
 * Subscribes a listener to the model event loop.
 * @param event String identifier of the event that will trigger the callback.
 * @param callback Action to perform when event happens.
 * @param deps Dependencies that should be kept up to date within the callback.
 */
const useModelEvent = (model, event, callback, deps) => {
    react_1.default.useEffect(() => {
        const callbackWrapper = (e) => model && callback(model, e);
        model === null || model === void 0 ? void 0 : model.on(event, callbackWrapper);
        return () => void (model === null || model === void 0 ? void 0 : model.unbind(event, callbackWrapper));
    }, (deps || []).concat([model]));
};
exports.useModelEvent = useModelEvent;
//# sourceMappingURL=hooks.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Fausto Morales
// Distributed under the terms of the MIT License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
exports.MODULE_VERSION = data.version;
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

module.exports = JSON.parse('{"name":"qslwidgets","version":"0.0.13","description":"Widgets for the QSL image labeling package.","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/faustomorales/qsl","bugs":{"url":"https://github.com/faustomorales/qsl/issues"},"license":"MIT","author":{"name":"Fausto Morales","email":"fausto@robinbay.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/faustomorales/qsl"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf qsl/labextension","clean:nbextension":"rimraf qsl/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","format":"prettier --write src","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","react":"^17.0.2","react-dom":"^17.0.2","react-image-labeler":"0.0.1-alpha.27","streamlit-component-lib":"^1.4.0"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@babel/preset-react":"^7.14.5","@babel/preset-typescript":"^7.14.5","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/react":"^17.0.11","@types/react-dom":"^17.0.8","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","babel-loader":"^8.2.2","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","html-webpack-plugin":"^5.5.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"babel":{"presets":["@babel/preset-env","@babel/preset-react","@babel/preset-typescript"]},"jupyterlab":{"extension":"lib/plugin","outputDir":"../qsl/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_ImageLabelerWidget_js.4f8985486b700d616f4c.js.map