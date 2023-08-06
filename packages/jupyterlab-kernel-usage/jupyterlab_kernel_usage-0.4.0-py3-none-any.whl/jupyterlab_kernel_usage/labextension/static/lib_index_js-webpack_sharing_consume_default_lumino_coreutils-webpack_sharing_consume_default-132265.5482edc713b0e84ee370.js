"use strict";
(self["webpackChunkjupyterlab_kernel_usage"] = self["webpackChunkjupyterlab_kernel_usage"] || []).push([["lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-132265"],{

/***/ "./lib/format.js":
/*!***********************!*\
  !*** ./lib/format.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "formatForDisplay": () => (/* binding */ formatForDisplay)
/* harmony export */ });
// Taken from https://github.com/jupyter-server/jupyter-resource-usage/blob/e6ec53fa69fdb6de8e878974bcff006310658408/packages/labextension/src/memoryUsage.tsx#L272
const MEMORY_UNIT_LIMITS = {
    B: 1,
    KB: 1024,
    MB: 1048576,
    GB: 1073741824,
    TB: 1099511627776,
    PB: 1125899906842624
};
function formatForDisplay(numBytes) {
    const lu = convertToLargestUnit(numBytes);
    return lu[0].toFixed(2) + ' ' + lu[1];
}
/**
 * Given a number of bytes, convert to the most human-readable
 * format, (GB, TB, etc).
 * Taken from https://github.com/jupyter-server/jupyter-resource-usage/blob/e6ec53fa69fdb6de8e878974bcff006310658408/packages/labextension/src/memoryUsage.tsx#L272
 */
function convertToLargestUnit(numBytes) {
    if (!numBytes) {
        return [0, 'B'];
    }
    if (numBytes < MEMORY_UNIT_LIMITS.KB) {
        return [numBytes, 'B'];
    }
    else if (MEMORY_UNIT_LIMITS.KB === numBytes ||
        numBytes < MEMORY_UNIT_LIMITS.MB) {
        return [numBytes / MEMORY_UNIT_LIMITS.KB, 'KB'];
    }
    else if (MEMORY_UNIT_LIMITS.MB === numBytes ||
        numBytes < MEMORY_UNIT_LIMITS.GB) {
        return [numBytes / MEMORY_UNIT_LIMITS.MB, 'MB'];
    }
    else if (MEMORY_UNIT_LIMITS.GB === numBytes ||
        numBytes < MEMORY_UNIT_LIMITS.TB) {
        return [numBytes / MEMORY_UNIT_LIMITS.GB, 'GB'];
    }
    else if (MEMORY_UNIT_LIMITS.TB === numBytes ||
        numBytes < MEMORY_UNIT_LIMITS.PB) {
        return [numBytes / MEMORY_UNIT_LIMITS.TB, 'TB'];
    }
    else {
        return [numBytes / MEMORY_UNIT_LIMITS.PB, 'PB'];
    }
}


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab_kernel_usage', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _panel__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./panel */ "./lib/panel.js");
/* harmony import */ var _style_tachometer_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/tachometer.svg */ "./style/tachometer.svg");






var CommandIDs;
(function (CommandIDs) {
    CommandIDs.getKernelUsage = 'kernel-usage:get';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the kernelusage extension.
 */
const plugin = {
    id: 'kernelusage:plugin',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher],
    autoStart: true,
    activate: (app, palette, notebookTracker, launcher) => {
        const { commands, shell } = app;
        const category = 'Kernel Resource';
        async function createPanel() {
            const panel = new _panel__WEBPACK_IMPORTED_MODULE_4__.KernelUsagePanel({
                widgetAdded: notebookTracker.widgetAdded,
                currentNotebookChanged: notebookTracker.currentChanged
            });
            shell.add(panel, 'right', { rank: 200 });
            return panel;
        }
        commands.addCommand(CommandIDs.getKernelUsage, {
            label: 'Kernel Usage',
            caption: 'Kernel Usage',
            icon: new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
                name: 'jupyterlab-kernel-usage:icon',
                svgstr: _style_tachometer_svg__WEBPACK_IMPORTED_MODULE_5__["default"]
            }),
            execute: createPanel
        });
        palette.addItem({ command: CommandIDs.getKernelUsage, category });
        createPanel();
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/panel.js":
/*!**********************!*\
  !*** ./lib/panel.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelUsagePanel": () => (/* binding */ KernelUsagePanel)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _style_tachometer_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/tachometer.svg */ "./style/tachometer.svg");




const PANEL_CLASS = 'jp-kernelusage-view';
class KernelUsagePanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.StackedPanel {
    constructor(props) {
        super();
        this.addClass(PANEL_CLASS);
        this.id = 'kernelusage-panel-id';
        this.title.caption = 'Kernel Usage';
        this.title.icon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
            name: 'jupyterlab-kernel-usage:icon',
            svgstr: _style_tachometer_svg__WEBPACK_IMPORTED_MODULE_2__["default"]
        });
        this.title.closable = true;
        const widget = new _widget__WEBPACK_IMPORTED_MODULE_3__.KernelUsageWidget({
            widgetAdded: props.widgetAdded,
            currentNotebookChanged: props.currentNotebookChanged
        });
        this.addWidget(widget);
    }
    dispose() {
        super.dispose();
    }
    onCloseRequest(msg) {
        super.onCloseRequest(msg);
        this.dispose();
    }
}


/***/ }),

/***/ "./lib/useInterval.js":
/*!****************************!*\
  !*** ./lib/useInterval.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const useInterval = (callback, delay) => {
    const savedCallback = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)();
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        savedCallback.current = callback;
    }, [callback]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        function tick() {
            if (savedCallback.current) {
                savedCallback.current();
            }
        }
        if (delay !== null) {
            const id = setInterval(tick, delay);
            return () => {
                clearInterval(id);
            };
        }
    }, [callback, delay]);
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (useInterval);


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelUsageWidget": () => (/* binding */ KernelUsageWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/polling */ "./node_modules/@lumino/polling/dist/index.es6.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _useInterval__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./useInterval */ "./lib/useInterval.js");
/* harmony import */ var _format__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./format */ "./lib/format.js");






const POLL_INTERVAL_SEC = 5;
const POLL_MAX_INTERVAL_SEC = 300;
const kernelPools = new Map();
const KernelUsage = (props) => {
    var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k, _l, _m, _o, _p;
    const [kernelId, setKernelId] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)();
    const [refresh, setRefresh] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(true);
    (0,_useInterval__WEBPACK_IMPORTED_MODULE_3__["default"])(async () => {
        setRefresh(!refresh);
    }, POLL_INTERVAL_SEC * 1000);
    const requestUsage = async (kernelId) => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)(`get_usage/${kernelId}`)
            .then(data => {
            const kernelPoll = kernelPools.get(kernelId);
            if (kernelPoll) {
                kernelPoll.usage = Object.assign(Object.assign({}, data.content), { kernelId, timestamp: new Date() });
                kernelPools.set(kernelId, kernelPoll);
            }
        })
            .catch(reason => {
            console.error(`The kernelusage server extension has returned an error.\n${reason}`);
            const kernelPoll = kernelPools.get(kernelId);
            kernelPoll === null || kernelPoll === void 0 ? void 0 : kernelPoll.poll.stop().then(() => {
                kernelPools.delete(kernelId);
            });
        });
    };
    const doPoll = (kernelId, path) => {
        let kernelPoll = kernelPools.get(kernelId);
        if (!kernelPoll) {
            const poll = new _lumino_polling__WEBPACK_IMPORTED_MODULE_1__.Poll({
                auto: true,
                factory: () => requestUsage(kernelId),
                frequency: {
                    interval: POLL_INTERVAL_SEC * 1000,
                    backoff: true,
                    max: POLL_MAX_INTERVAL_SEC * 1000
                },
                name: `@jupyterlab/kernel:KernelUsage#${kernelId}`,
                standby: 'never'
            });
            kernelPoll = {
                poll,
                path,
                usage: undefined
            };
            kernelPools.set(kernelId, kernelPoll);
        }
    };
    props.currentNotebookChanged.connect((sender, panel) => {
        var _a, _b, _c, _d, _e, _f;
        panel === null || panel === void 0 ? void 0 : panel.sessionContext.kernelChanged.connect((_sender, args) => {
            var _a, _b;
            const kernelId = (_a = args.newValue) === null || _a === void 0 ? void 0 : _a.id;
            if (kernelId) {
                setKernelId(kernelId);
                const path = (_b = panel === null || panel === void 0 ? void 0 : panel.sessionContext.session) === null || _b === void 0 ? void 0 : _b.model.path;
                doPoll(kernelId, path);
            }
        });
        if (((_a = panel === null || panel === void 0 ? void 0 : panel.sessionContext.session) === null || _a === void 0 ? void 0 : _a.id) !== kernelId) {
            if ((_c = (_b = panel === null || panel === void 0 ? void 0 : panel.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.id) {
                const kernelId = (_e = (_d = panel === null || panel === void 0 ? void 0 : panel.sessionContext.session) === null || _d === void 0 ? void 0 : _d.kernel) === null || _e === void 0 ? void 0 : _e.id;
                if (kernelId) {
                    setKernelId(kernelId);
                    const path = (_f = panel === null || panel === void 0 ? void 0 : panel.sessionContext.session) === null || _f === void 0 ? void 0 : _f.model.path;
                    doPoll(kernelId, path);
                }
            }
        }
    });
    if (kernelId) {
        const kernelPoll = kernelPools.get(kernelId);
        if (kernelPoll) {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h3", { className: "jp-kernelusage-separator" }, "Kernel Usage"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Kernel Host: ", (_a = kernelPoll.usage) === null || _a === void 0 ? void 0 :
                    _a.hostname),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Notebook: ",
                    kernelPoll.path),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Kernel ID: ",
                    kernelId),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Timestamp: ", (_c = (_b = kernelPoll.usage) === null || _b === void 0 ? void 0 : _b.timestamp) === null || _c === void 0 ? void 0 :
                    _c.toLocaleString()),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "CPU: ", (_d = kernelPoll.usage) === null || _d === void 0 ? void 0 :
                    _d.kernel_cpu.toFixed(1)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Memory: ",
                    (0,_format__WEBPACK_IMPORTED_MODULE_5__.formatForDisplay)((_e = kernelPoll.usage) === null || _e === void 0 ? void 0 : _e.kernel_memory)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("hr", null),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h4", { className: "jp-kernelusage-separator" }, "Host CPU"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Percentage ", (_f = kernelPoll.usage) === null || _f === void 0 ? void 0 :
                    _f.host_cpu_percent.toFixed(1)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h4", { className: "jp-kernelusage-separator" }, "Host Virtual Memory"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Active:",
                    ' ',
                    (0,_format__WEBPACK_IMPORTED_MODULE_5__.formatForDisplay)((_g = kernelPoll.usage) === null || _g === void 0 ? void 0 : _g.host_virtual_memory.active)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Available:",
                    ' ',
                    (0,_format__WEBPACK_IMPORTED_MODULE_5__.formatForDisplay)((_h = kernelPoll.usage) === null || _h === void 0 ? void 0 : _h.host_virtual_memory.available)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Free:",
                    ' ',
                    (0,_format__WEBPACK_IMPORTED_MODULE_5__.formatForDisplay)((_j = kernelPoll.usage) === null || _j === void 0 ? void 0 : _j.host_virtual_memory.free)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Inactive:",
                    ' ',
                    (0,_format__WEBPACK_IMPORTED_MODULE_5__.formatForDisplay)((_k = kernelPoll.usage) === null || _k === void 0 ? void 0 : _k.host_virtual_memory.inactive)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Percent: ", (_l = kernelPoll.usage) === null || _l === void 0 ? void 0 :
                    _l.host_virtual_memory.percent.toFixed(1)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Total:",
                    ' ',
                    (0,_format__WEBPACK_IMPORTED_MODULE_5__.formatForDisplay)((_m = kernelPoll.usage) === null || _m === void 0 ? void 0 : _m.host_virtual_memory.total)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Used:",
                    ' ',
                    (0,_format__WEBPACK_IMPORTED_MODULE_5__.formatForDisplay)((_o = kernelPoll.usage) === null || _o === void 0 ? void 0 : _o.host_virtual_memory.used)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-kernelusage-separator" },
                    "Wired:",
                    ' ',
                    (0,_format__WEBPACK_IMPORTED_MODULE_5__.formatForDisplay)((_p = kernelPoll.usage) === null || _p === void 0 ? void 0 : _p.host_virtual_memory.wired))));
        }
    }
    return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h3", null, "Kernel usage is not available");
};
class KernelUsageWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ReactWidget {
    constructor(props) {
        super();
        this._widgetAdded = props.widgetAdded;
        this._currentNotebookChanged = props.currentNotebookChanged;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(KernelUsage, { widgetAdded: this._widgetAdded, currentNotebookChanged: this._currentNotebookChanged }));
    }
}


/***/ }),

/***/ "./style/tachometer.svg":
/*!******************************!*\
  !*** ./style/tachometer.svg ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<!-- Generator: Adobe Illustrator 21.0.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->\r\n<svg version=\"1.1\" id=\"Layer_1\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\"\r\n\t viewBox=\"0 0 512 512\" style=\"enable-background:new 0 0 512 512;\" xml:space=\"preserve\">\r\n<g>\r\n\t<path d=\"M256,42.7c-141.2,0-256,114.8-256,256c0,61.8,22.1,118.4,58.7,162.7l6,8h382.7l6-8c36.6-44.3,58.7-100.9,58.7-162.7\r\n\t\tC512,157.5,397.2,42.7,256,42.7z M256,85.3c118.1,0,213.3,95.2,213.3,213.3c0,48.3-16.9,92.3-44,128H86.7\r\n\t\tc-27.1-35.8-44-79.7-44-128C42.7,180.6,137.9,85.3,256,85.3z M256,106.7c-11.8,0-21.3,9.6-21.3,21.3s9.6,21.3,21.3,21.3\r\n\t\ts21.3-9.6,21.3-21.3S267.8,106.7,256,106.7z M170.7,129.3c-11.8,0-21.3,9.6-21.3,21.3s9.6,21.3,21.3,21.3s21.3-9.6,21.3-21.3\r\n\t\tS182.4,129.3,170.7,129.3z M341.3,129.3c-11.8,0-21.3,9.6-21.3,21.3s9.6,21.3,21.3,21.3s21.3-9.6,21.3-21.3\r\n\t\tS353.1,129.3,341.3,129.3z M108,192c-11.8,0-21.3,9.6-21.3,21.3s9.6,21.3,21.3,21.3s21.3-9.6,21.3-21.3S119.8,192,108,192z\r\n\t\t M398,192.7L277.3,262c-6.3-3.7-13.6-6-21.3-6c-23.6,0-42.7,19.1-42.7,42.7c0,23.6,19.1,42.7,42.7,42.7c23.3,0,42.3-18.8,42.7-42\r\n\t\tv-0.7L419.3,230L398,192.7z M85.3,277.3c-11.8,0-21.3,9.6-21.3,21.3S73.6,320,85.3,320s21.3-9.6,21.3-21.3S97.1,277.3,85.3,277.3z\r\n\t\t M426.7,277.3c-11.8,0-21.3,9.6-21.3,21.3s9.6,21.3,21.3,21.3s21.3-9.6,21.3-21.3S438.4,277.3,426.7,277.3z M108,362.7\r\n\t\tc-11.8,0-21.3,9.6-21.3,21.3s9.6,21.3,21.3,21.3s21.3-9.6,21.3-21.3S119.8,362.7,108,362.7z M404,362.7c-11.8,0-21.3,9.6-21.3,21.3\r\n\t\ts9.6,21.3,21.3,21.3s21.3-9.6,21.3-21.3S415.8,362.7,404,362.7z\"/>\r\n</g>\r\n</svg>\r\n\r\n<!--\r\nDownloaded from https://seekicon.com/free-icon/tachometer-alt_1 under MIT License.\r\n-->");

/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-132265.5482edc713b0e84ee370.js.map