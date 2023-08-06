"use strict";
(self["webpackChunkqslwidgets"] = self["webpackChunkqslwidgets"] || []).push([["lib_plugin_js"],{

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Fausto Morales
// Distributed under the terms of the MIT License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const ImageLabelerWidget_1 = __webpack_require__(/*! ./ImageLabelerWidget */ "./lib/ImageLabelerWidget.js");
const EXTENSION_ID = "qsl:plugin";
/**
 * The example plugin.
 */
const qslPlugin = {
    id: EXTENSION_ID,
    requires: [base_1.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true,
};
exports["default"] = qslPlugin;
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, registry) {
    registry.registerWidget({
        name: version_1.MODULE_NAME,
        version: version_1.MODULE_VERSION,
        exports: { ImageLabelerModel: ImageLabelerWidget_1.ImageLabelerModel, ImageLabelerView: ImageLabelerWidget_1.ImageLabelerView },
    });
}
//# sourceMappingURL=plugin.js.map

/***/ })

}]);
//# sourceMappingURL=lib_plugin_js.e0feae78489824b0e2c1.js.map