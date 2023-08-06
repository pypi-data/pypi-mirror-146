"use strict";
(self["webpackChunkjupyterlab_blockly"] = self["webpackChunkjupyterlab_blockly"] || []).push([["lib_index_js"],{

/***/ "./lib/factory.js":
/*!************************!*\
  !*** ./lib/factory.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BlocklyEditorFactory": () => (/* binding */ BlocklyEditorFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./manager */ "./lib/manager.js");



/**
 * A widget factory to create new instances of BlocklyEditor.
 */
class BlocklyEditorFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.ABCWidgetFactory {
    /**
     * Constructor of BlocklyEditorFactory.
     *
     * @param options Constructor options
     */
    constructor(options) {
        super(options);
        this._manager = new _manager__WEBPACK_IMPORTED_MODULE_1__.BlocklyManager();
        this._rendermime = options.rendermime;
    }
    get manager() {
        return this._manager;
    }
    /**
     * Create a new widget given a context.
     *
     * @param context Contains the information of the file
     * @returns The widget
     */
    createNewWidget(context) {
        return new _widget__WEBPACK_IMPORTED_MODULE_2__.BlocklyEditor({
            context,
            content: new _widget__WEBPACK_IMPORTED_MODULE_2__.BlocklyPanel(context, this._manager, this._rendermime)
        });
    }
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
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _factory__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./factory */ "./lib/factory.js");
/* harmony import */ var _token__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./token */ "./lib/token.js");





/**
 * The name of the factory that creates the editor widgets.
 */
const FACTORY = 'Blockly editor';
/**
 * Initialization data for the jupyterlab-blocky extension.
 */
const plugin = {
    id: 'jupyterlab-blocky:plugin',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.IRenderMimeRegistry],
    provides: _token__WEBPACK_IMPORTED_MODULE_3__.IBlocklyManager,
    activate: (app, restorer, rendermime) => {
        console.log('JupyterLab extension jupyterlab-blocky is activated!');
        // Namespace for the tracker
        const namespace = 'jupyterlab-blocky';
        // Creating the tracker for the document
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({ namespace });
        // Handle state restoration.
        if (restorer) {
            // When restoring the app, if the document was open, reopen it
            restorer.restore(tracker, {
                command: 'docmanager:open',
                args: widget => ({ path: widget.context.path, factory: FACTORY }),
                name: widget => widget.context.path
            });
        }
        // Creating the widget factory to register it so the document manager knows about
        // our new DocumentWidget
        const widgetFactory = new _factory__WEBPACK_IMPORTED_MODULE_4__.BlocklyEditorFactory({
            name: FACTORY,
            modelName: 'text',
            fileTypes: ['json'],
            defaultFor: ['json'],
            // Kernel options, in this case we need to execute the code generated
            // in the blockly editor. The best way would be to use kernels, for
            // that reason, we tell the widget factory to start a kernel session
            // when opening the editor, and close the session when closing the editor.
            canStartKernel: true,
            preferKernel: true,
            shutdownOnClose: true,
            // The rendermime instance, necessary to render the outputs
            // after a code execution.
            rendermime: rendermime
        });
        // Add the widget to the tracker when it's created
        widgetFactory.widgetCreated.connect((sender, widget) => {
            // Notify the instance tracker if restore data needs to update.
            widget.context.pathChanged.connect(() => {
                tracker.save(widget);
            });
            tracker.add(widget);
        });
        // Registering the widget factory
        app.docRegistry.addWidgetFactory(widgetFactory);
        return widgetFactory.manager;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/layout.js":
/*!***********************!*\
  !*** ./lib/layout.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BlocklyLayout": () => (/* binding */ BlocklyLayout)
/* harmony export */ });
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");





/**
 * A blockly layout to host the Blockly editor.
 */
class BlocklyLayout extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.PanelLayout {
    /**
     * Construct a `BlocklyLayout`.
     *
     */
    constructor(manager, sessionContext, rendermime) {
        super();
        this._manager = manager;
        this._sessionContext = sessionContext;
        // Creating the container for the Blockly editor
        // and the output area to render the execution replies.
        this._host = document.createElement('div');
        // Creating a SimplifiedOutputArea widget to render the
        // outputs from the execution reply.
        this._outputArea = new _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.SimplifiedOutputArea({
            model: new _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputAreaModel({ trusted: true }),
            rendermime
        });
    }
    get workspace() {
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        return blockly__WEBPACK_IMPORTED_MODULE_3__.serialization.workspaces.save(this._workspace);
    }
    set workspace(workspace) {
        // eslint-disable-next-line @typescript-eslint/ban-ts-comment
        // @ts-ignore
        blockly__WEBPACK_IMPORTED_MODULE_3__.serialization.workspaces.load(workspace, this._workspace);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        this._workspace.dispose();
        super.dispose();
    }
    /**
     * Init the blockly layout
     */
    init() {
        super.init();
        // Add the blockly container into the DOM
        this.addWidget(new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget({ node: this._host }));
    }
    /**
     * Create an iterator over the widgets in the layout.
     */
    iter() {
        return new _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.ArrayIterator([]);
    }
    /**
     * Remove a widget from the layout.
     *
     * @param widget - The `widget` to remove.
     */
    removeWidget(widget) {
        return;
    }
    run() {
        // Serializing our workspace into the chosen language generator.
        const code = this._manager.generator.workspaceToCode(this._workspace);
        // Execute the code using the kernel, by using a static method from the
        // same class to make an execution request.
        _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.SimplifiedOutputArea.execute(code, this._outputArea, this._sessionContext)
            .then(resp => {
            this.addWidget(this._outputArea);
            this._resizeWorkspace();
        })
            .catch(e => console.error(e));
    }
    /**
     * Handle `update-request` messages sent to the widget.
     */
    onUpdateRequest(msg) {
        this._resizeWorkspace();
    }
    /**
     * Handle `resize-request` messages sent to the widget.
     */
    onResize(msg) {
        this._resizeWorkspace();
    }
    /**
     * Handle `fit-request` messages sent to the widget.
     */
    onFitRequest(msg) {
        this._resizeWorkspace();
    }
    /**
     * Handle `after-attach` messages sent to the widget.
     */
    onAfterAttach(msg) {
        //inject Blockly with appropiate JupyterLab theme.
        this._workspace = blockly__WEBPACK_IMPORTED_MODULE_3__.inject(this._host, {
            toolbox: this._manager.toolbox,
            theme: _utils__WEBPACK_IMPORTED_MODULE_4__.THEME
        });
    }
    _resizeWorkspace() {
        //Resize logic.
        const rect = this.parent.node.getBoundingClientRect();
        const { height } = this._outputArea.node.getBoundingClientRect();
        this._host.style.width = rect.width + 'px';
        const margin = rect.height / 3;
        if (height > margin) {
            this._host.style.height = rect.height - margin + 'px';
            this._outputArea.node.style.height = margin + 'px';
            this._outputArea.node.style.overflowY = 'scroll';
        }
        else {
            this._host.style.height = rect.height - height + 'px';
            this._outputArea.node.style.overflowY = 'hidden';
        }
        blockly__WEBPACK_IMPORTED_MODULE_3__.svgResize(this._workspace);
    }
}


/***/ }),

/***/ "./lib/manager.js":
/*!************************!*\
  !*** ./lib/manager.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BlocklyManager": () => (/* binding */ BlocklyManager)
/* harmony export */ });
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! blockly/python */ "./node_modules/blockly/python.js");
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(blockly_python__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");



class BlocklyManager {
    /**
     * Constructor of BlocklyEditorFactory.
     *
     * @param options Constructor options
     */
    constructor() {
        this._toolbox = _utils__WEBPACK_IMPORTED_MODULE_2__.TOOLBOX;
        this._activeGenerator = (blockly_python__WEBPACK_IMPORTED_MODULE_1___default());
        this._generators = new Map();
    }
    get toolbox() {
        return this._toolbox;
    }
    set activeGenerator(name) {
        this._activeGenerator = this._generators.get(name);
    }
    get generator() {
        return this._activeGenerator;
    }
    registerToolbox(value) {
        this._toolbox = value;
    }
    registerBlocks(blocks) {
        blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray(blocks);
    }
    registerGenerator(kernel, generator) {
        this._generators.set(kernel, generator);
    }
}


/***/ }),

/***/ "./lib/token.js":
/*!**********************!*\
  !*** ./lib/token.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IBlocklyManager": () => (/* binding */ IBlocklyManager)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The manager token.
 */
const IBlocklyManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('jupyterlab-blockly/manager');


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TOOLBOX": () => (/* binding */ TOOLBOX),
/* harmony export */   "THEME": () => (/* binding */ THEME)
/* harmony export */ });
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_0__);

// Creating a toolbox containing all the main (default) blocks.
const TOOLBOX = {
    kind: 'categoryToolbox',
    contents: [
        {
            kind: 'category',
            name: 'Logic',
            colour: '210',
            contents: [
                {
                    kind: 'block',
                    type: 'controls_if'
                },
                {
                    kind: 'BLOCK',
                    type: 'logic_compare'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_operation"></block>',
                    type: 'logic_operation'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_negate"></block>',
                    type: 'logic_negate'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_boolean"></block>',
                    type: 'logic_boolean'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_null"></block>',
                    type: 'logic_null'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="logic_ternary"></block>',
                    type: 'logic_ternary'
                }
            ]
        },
        {
            kind: 'category',
            name: 'Loops',
            colour: '120',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_repeat_ext">\n          <value name="TIMES">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'controls_repeat_ext'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_whileUntil"></block>',
                    type: 'controls_whileUntil'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_for">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n          <value name="BY">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'controls_for'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_forEach"></block>',
                    type: 'controls_forEach'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="controls_flow_statements"></block>',
                    type: 'controls_flow_statements'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Math',
            colour: '230',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_number"></block>',
                    type: 'math_number'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_arithmetic">\n          <value name="A">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="B">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_arithmetic'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_single">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">9</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_single'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_trig">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">45</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_trig'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_constant"></block>',
                    type: 'math_constant'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_number_property">\n          <value name="NUMBER_TO_CHECK">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_number_property'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_change">\n          <value name="DELTA">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_change'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_round">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">3.1</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_round'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_on_list"></block>',
                    type: 'math_on_list'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_modulo">\n          <value name="DIVIDEND">\n            <shadow type="math_number">\n              <field name="NUM">64</field>\n            </shadow>\n          </value>\n          <value name="DIVISOR">\n            <shadow type="math_number">\n              <field name="NUM">10</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_modulo'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_constrain">\n          <value name="VALUE">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="LOW">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="HIGH">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_constrain'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_random_int">\n          <value name="FROM">\n            <shadow type="math_number">\n              <field name="NUM">1</field>\n            </shadow>\n          </value>\n          <value name="TO">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'math_random_int'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="math_random_float"></block>',
                    type: 'math_random_float'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Text',
            colour: '160',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text"></block>',
                    type: 'text'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_join"></block>',
                    type: 'text_join'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_append">\n          <value name="TEXT">\n            <shadow type="text"></shadow>\n          </value>\n        </block>',
                    type: 'text_append'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_length">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_length'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_isEmpty">\n          <value name="VALUE">\n            <shadow type="text">\n              <field name="TEXT"></field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_isEmpty'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n          <value name="FIND">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_indexOf'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_charAt">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
                    type: 'text_charAt'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_getSubstring">\n          <value name="STRING">\n            <block type="variables_get">\n              <field name="VAR">text</field>\n            </block>\n          </value>\n        </block>',
                    type: 'text_getSubstring'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_changeCase">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_changeCase'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_trim">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_trim'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_print">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_print'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="text_prompt_ext">\n          <value name="TEXT">\n            <shadow type="text">\n              <field name="TEXT">abc</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'text_prompt_ext'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Lists',
            colour: '260',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_create_with">\n          <mutation items="0"></mutation>\n        </block>',
                    type: 'lists_create_with'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_create_with"></block>',
                    type: 'lists_create_with'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_repeat">\n          <value name="NUM">\n            <shadow type="math_number">\n              <field name="NUM">5</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'lists_repeat'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_length"></block>',
                    type: 'lists_length'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_isEmpty"></block>',
                    type: 'lists_isEmpty'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_indexOf">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_indexOf'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_getIndex">\n          <value name="VALUE">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_getIndex'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_setIndex">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_setIndex'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_getSublist">\n          <value name="LIST">\n            <block type="variables_get">\n              <field name="VAR">list</field>\n            </block>\n          </value>\n        </block>',
                    type: 'lists_getSublist'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_split">\n          <value name="DELIM">\n            <shadow type="text">\n              <field name="TEXT">,</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'lists_split'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="lists_sort"></block>',
                    type: 'lists_sort'
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: 'Color',
            colour: '20',
            contents: [
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_picker"></block>',
                    type: 'colour_picker'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_random"></block>',
                    type: 'colour_random'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_rgb">\n          <value name="RED">\n            <shadow type="math_number">\n              <field name="NUM">100</field>\n            </shadow>\n          </value>\n          <value name="GREEN">\n            <shadow type="math_number">\n              <field name="NUM">50</field>\n            </shadow>\n          </value>\n          <value name="BLUE">\n            <shadow type="math_number">\n              <field name="NUM">0</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'colour_rgb'
                },
                {
                    kind: 'BLOCK',
                    blockxml: '<block type="colour_blend">\n          <value name="COLOUR1">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#ff0000</field>\n            </shadow>\n          </value>\n          <value name="COLOUR2">\n            <shadow type="colour_picker">\n              <field name="COLOUR">#3333ff</field>\n            </shadow>\n          </value>\n          <value name="RATIO">\n            <shadow type="math_number">\n              <field name="NUM">0.5</field>\n            </shadow>\n          </value>\n        </block>',
                    type: 'colour_blend'
                }
            ]
        },
        {
            kind: 'SEP'
        },
        {
            kind: 'CATEGORY',
            colour: '330',
            custom: 'VARIABLE',
            name: 'Variables'
        },
        {
            kind: 'CATEGORY',
            colour: '290',
            custom: 'PROCEDURE',
            name: 'Functions'
        }
    ]
};
// Defining a Blockly Theme in accordance with the current JupyterLab Theme.
const jupyterlab_theme = blockly__WEBPACK_IMPORTED_MODULE_0__.Theme.defineTheme('jupyterlab', {
    base: blockly__WEBPACK_IMPORTED_MODULE_0__.Themes.Classic,
    componentStyles: {
        workspaceBackgroundColour: 'var(--jp-layout-color0)',
        toolboxBackgroundColour: 'var(--jp-layout-color2)',
        toolboxForegroundColour: 'var(--jp-ui-font-color0)',
        flyoutBackgroundColour: 'var(--jp-border-color2)',
        flyoutForegroundColour: 'var(--jp-layout-color3)',
        flyoutOpacity: 1,
        scrollbarColour: 'var(--jp-border-color0)',
        insertionMarkerOpacity: 0.3,
        scrollbarOpacity: 0.4,
        cursorColour: 'var(--jp-scrollbar-background-color)'
    }
});
const THEME = jupyterlab_theme;


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BlocklyEditor": () => (/* binding */ BlocklyEditor),
/* harmony export */   "BlocklyPanel": () => (/* binding */ BlocklyPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _layout__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./layout */ "./lib/layout.js");






/**
 * DocumentWidget: widget that represents the view or editor for a file type.
 */
class BlocklyEditor extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.DocumentWidget {
    constructor(options) {
        super(options);
        // Create and add a button to the toolbar to execute
        // the code.
        const runCode = () => {
            this.content.layout.run();
        };
        const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            label: 'Run Code',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.runIcon,
            className: 'jp-blockly-button',
            onClick: runCode,
            tooltip: 'Run Code'
        });
        button.addClass('jp-blockly-runButton');
        this.toolbar.addItem('run', button);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        this.content.dispose();
        super.dispose();
    }
}
/**
 * Widget that contains the main view of the DocumentWidget.
 */
class BlocklyPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Panel {
    /**
     * Construct a `ExamplePanel`.
     *
     * @param context - The documents context.
     */
    constructor(context, manager, rendermime) {
        super({
            layout: new _layout__WEBPACK_IMPORTED_MODULE_5__.BlocklyLayout(manager, context.sessionContext, rendermime)
        });
        this.addClass('jp-BlocklyPanel');
        this._context = context;
        // Load the content of the file when the context is ready
        this._context.ready.then(() => this._load());
        // Connect to the save signal
        this._context.saveState.connect(this._onSave, this);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal.clearData(this);
        super.dispose();
    }
    _load() {
        // Loading the content of the document into the workspace
        const content = this._context.model.toJSON();
        this.layout.workspace = content;
    }
    _onSave(sender, state) {
        if (state === 'started') {
            const workspace = this.layout.workspace;
            this._context.model.fromJSON(workspace);
        }
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.7ff68a49ec6ed2f13dc1.js.map