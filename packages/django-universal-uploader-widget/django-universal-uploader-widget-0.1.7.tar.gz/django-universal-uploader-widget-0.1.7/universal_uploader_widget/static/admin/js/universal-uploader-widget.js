/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/UniversalUploaderWidget.scss":
/*!******************************************!*\
  !*** ./src/UniversalUploaderWidget.scss ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n// extracted by mini-css-extract-plugin\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/UniversalUploaderWidget.scss?");

/***/ }),

/***/ "./src/Icons/DeleteIcon.ts":
/*!*********************************!*\
  !*** ./src/Icons/DeleteIcon.ts ***!
  \*********************************/
/***/ ((__unused_webpack_module, exports) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports[\"default\"] = '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 512 512\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:space=\"preserve\" width=\"100%\" height=\"100%\"><path xmlns=\"http://www.w3.org/2000/svg\" d=\"m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z\"></path></svg>';\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/Icons/DeleteIcon.ts?");

/***/ }),

/***/ "./src/Icons/PreviewIcon.ts":
/*!**********************************!*\
  !*** ./src/Icons/PreviewIcon.ts ***!
  \**********************************/
/***/ ((__unused_webpack_module, exports) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports[\"default\"] = '<svg xmlns=\"http://www.w3.org/2000/svg\" fill=\"currentColor\" class=\"bi bi-zoom-in\" viewBox=\"0 0 16 16\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:space=\"preserve\" width=\"100%\" height=\"100%\"><path xmlns=\"http://www.w3.org/2000/svg\" fill-rule=\"evenodd\" d=\"M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11zM13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0z\"></path><path xmlns=\"http://www.w3.org/2000/svg\" d=\"M10.344 11.742c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1 6.538 6.538 0 0 1-1.398 1.4z\"></path><path xmlns=\"http://www.w3.org/2000/svg\" fill-rule=\"evenodd\" d=\"M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5z\"></path></svg>';\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/Icons/PreviewIcon.ts?");

/***/ }),

/***/ "./src/Preview/Preview.ts":
/*!********************************!*\
  !*** ./src/Preview/Preview.ts ***!
  \********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

eval("\nvar __importDefault = (this && this.__importDefault) || function (mod) {\n    return (mod && mod.__esModule) ? mod : { \"default\": mod };\n};\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports.renderPreview = void 0;\nconst DeleteIcon_1 = __importDefault(__webpack_require__(/*! ../Icons/DeleteIcon */ \"./src/Icons/DeleteIcon.ts\"));\nconst PreviewIcon_1 = __importDefault(__webpack_require__(/*! ../Icons/PreviewIcon */ \"./src/Icons/PreviewIcon.ts\"));\nfunction renderPreview(url, canDelete, canPreview) {\n    // create preview\n    const preview = document.createElement('div');\n    preview.classList.add('uuw-file-preview');\n    // create img\n    const img = document.createElement('img');\n    img.src = url;\n    preview.appendChild(img);\n    // create delete icon\n    if (canDelete) {\n        const span = document.createElement('span');\n        span.classList.add('uuw-delete-icon');\n        span.innerHTML = DeleteIcon_1.default;\n        preview.appendChild(span);\n    }\n    // create preview icon\n    if (canPreview) {\n        const span = document.createElement('span');\n        span.classList.add('uuw-preview-icon');\n        if (!canDelete) {\n            span.classList.add('uuw-only-preview');\n        }\n        span.innerHTML = PreviewIcon_1.default;\n        preview.appendChild(span);\n    }\n    return preview;\n}\nexports.renderPreview = renderPreview;\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/Preview/Preview.ts?");

/***/ }),

/***/ "./src/Preview/index.ts":
/*!******************************!*\
  !*** ./src/Preview/index.ts ***!
  \******************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

eval("\nvar __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {\n    if (k2 === undefined) k2 = k;\n    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });\n}) : (function(o, m, k, k2) {\n    if (k2 === undefined) k2 = k;\n    o[k2] = m[k];\n}));\nvar __exportStar = (this && this.__exportStar) || function(m, exports) {\n    for (var p in m) if (p !== \"default\" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);\n};\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\n__exportStar(__webpack_require__(/*! ./Preview */ \"./src/Preview/Preview.ts\"), exports);\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/Preview/index.ts?");

/***/ }),

/***/ "./src/PreviewModal/PreviewModal.ts":
/*!******************************************!*\
  !*** ./src/PreviewModal/PreviewModal.ts ***!
  \******************************************/
/***/ ((__unused_webpack_module, exports) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports.PreviewModal = void 0;\nexports.PreviewModal = {\n    openPreviewModal: () => {\n        const modal = document.getElementById(\"uuw-modal-element\");\n        if (!modal) {\n            return;\n        }\n        setTimeout(() => {\n            modal.classList.add(\"visible\");\n            modal.classList.remove(\"hide\");\n            document.body.style.overflow = \"hidden\";\n        }, 50);\n    },\n    closePreviewModal: () => {\n        document.body.style.overflow = \"auto\";\n        const modal = document.getElementById(\"uuw-modal-element\");\n        if (modal) {\n            modal.classList.remove(\"visible\");\n            modal.classList.add(\"hide\");\n            setTimeout(() => {\n                var _a;\n                (_a = modal.parentElement) === null || _a === void 0 ? void 0 : _a.removeChild(modal);\n            }, 300);\n        }\n    },\n    onModalClick: (e) => {\n        if (e && e.target) {\n            const element = e.target;\n            if (element.closest(\"img.uuw-modal-file-preview-item, canvas.uuw-modal-file-preview-item\")) {\n                return;\n            }\n        }\n        exports.PreviewModal.closePreviewModal();\n    },\n    createPreviewModal: (file) => {\n        file.className = \"\";\n        file.classList.add(\"uuw-modal-file-preview-item\");\n        const modal = document.createElement(\"div\");\n        modal.id = \"uuw-modal-element\";\n        modal.classList.add(\"uuw-modal\", \"hide\");\n        modal.addEventListener(\"click\", exports.PreviewModal.onModalClick);\n        const preview = document.createElement(\"div\");\n        preview.classList.add(\"uuw-modal-file-preview\");\n        preview.innerHTML =\n            '<span class=\"uuw-modal-close\"><svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 512 512\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" xml:space=\"preserve\" width=\"100%\" height=\"100%\"><path xmlns=\"http://www.w3.org/2000/svg\" d=\"m289.94 256 95-95A24 24 0 0 0 351 127l-95 95-95-95a24 24 0 0 0-34 34l95 95-95 95a24 24 0 1 0 34 34l95-95 95 95a24 24 0 0 0 34-34z\"></path></svg></span>';\n        preview.appendChild(file);\n        modal.appendChild(preview);\n        document.body.appendChild(modal);\n        return modal;\n    },\n};\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/PreviewModal/PreviewModal.ts?");

/***/ }),

/***/ "./src/PreviewModal/index.ts":
/*!***********************************!*\
  !*** ./src/PreviewModal/index.ts ***!
  \***********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

eval("\nvar __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {\n    if (k2 === undefined) k2 = k;\n    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });\n}) : (function(o, m, k, k2) {\n    if (k2 === undefined) k2 = k;\n    o[k2] = m[k];\n}));\nvar __exportStar = (this && this.__exportStar) || function(m, exports) {\n    for (var p in m) if (p !== \"default\" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);\n};\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\n__exportStar(__webpack_require__(/*! ./PreviewModal */ \"./src/PreviewModal/PreviewModal.ts\"), exports);\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/PreviewModal/index.ts?");

/***/ }),

/***/ "./src/UniversalUploaderWidget.ts":
/*!****************************************!*\
  !*** ./src/UniversalUploaderWidget.ts ***!
  \****************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nconst ImageUploaderWidget_1 = __webpack_require__(/*! ./Widget/ImageUploaderWidget */ \"./src/Widget/ImageUploaderWidget/index.ts\");\nconst PdfUploaderWidget_1 = __webpack_require__(/*! ./Widget/PdfUploaderWidget */ \"./src/Widget/PdfUploaderWidget/index.ts\");\ndocument.addEventListener(\"DOMContentLoaded\", () => {\n    Array.from(document.querySelectorAll(\".uuw-root\")).map((element) => {\n        if (element.classList.contains(\"uuw-image\")) {\n            return new ImageUploaderWidget_1.ImageUploaderWidget(element);\n        }\n        else if (element.classList.contains(\"uuw-pdf\")) {\n            return new PdfUploaderWidget_1.PdfUploaderWidget(element);\n        }\n    });\n    if (window && window.django && window.django.jQuery) {\n        const $ = window.django.jQuery;\n        $(document).on(\"formset:added\", (_, row) => {\n            if (!row.length) {\n                return;\n            }\n            Array.from(row[0].querySelectorAll(\".uuw-root\")).map((element) => {\n                if (element.classList.contains(\"uuw-image\")) {\n                    return new ImageUploaderWidget_1.ImageUploaderWidget(element);\n                }\n                else if (element.classList.contains(\"uuw-pdf\")) {\n                    return new PdfUploaderWidget_1.PdfUploaderWidget(element);\n                }\n            });\n        });\n    }\n});\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/UniversalUploaderWidget.ts?");

/***/ }),

/***/ "./src/Widget/ImageUploaderWidget/ImageUploaderWidget.ts":
/*!***************************************************************!*\
  !*** ./src/Widget/ImageUploaderWidget/ImageUploaderWidget.ts ***!
  \***************************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports.ImageUploaderWidget = void 0;\nconst PreviewModal_1 = __webpack_require__(/*! ../../PreviewModal */ \"./src/PreviewModal/index.ts\");\nconst Preview_1 = __webpack_require__(/*! ../../Preview */ \"./src/Preview/index.ts\");\nclass ImageUploaderWidget {\n    constructor(element) {\n        this.canDelete = false;\n        this.dragging = false;\n        this.canPreview = true;\n        this.raw = null;\n        this.file = null;\n        this.performDeleteImage = (previewElement) => {\n            var _a;\n            (_a = previewElement === null || previewElement === void 0 ? void 0 : previewElement.parentElement) === null || _a === void 0 ? void 0 : _a.removeChild(previewElement);\n            if (this.checkboxInput) {\n                this.checkboxInput.checked = true;\n            }\n            this.fileInput.value = \"\";\n            this.file = null;\n            this.raw = null;\n            this.renderWidget();\n        };\n        this.performPreviewImage = (previewElement) => {\n            let image = previewElement === null || previewElement === void 0 ? void 0 : previewElement.querySelector(\"img\");\n            if (image) {\n                image = image.cloneNode(true);\n                PreviewModal_1.PreviewModal.createPreviewModal(image);\n                PreviewModal_1.PreviewModal.openPreviewModal();\n            }\n        };\n        this.onEmptyMarkerClick = () => {\n            this.fileInput.click();\n        };\n        this.onDrop = (e) => {\n            var _a;\n            e.preventDefault();\n            this.dragging = false;\n            this.element.classList.remove(\"drop-zone\");\n            if ((_a = e.dataTransfer) === null || _a === void 0 ? void 0 : _a.files.length) {\n                this.fileInput.files = e.dataTransfer.files;\n                this.file = this.fileInput.files[0];\n                this.raw = null;\n                this.renderWidget();\n            }\n        };\n        this.onDragEnter = () => {\n            this.dragging = true;\n            this.element.classList.add(\"drop-zone\");\n        };\n        this.onDragOver = (e) => {\n            if (e) {\n                e.preventDefault();\n            }\n        };\n        this.onDragLeave = (e) => {\n            if (e.relatedTarget &&\n                e.relatedTarget.closest(\".uuw-root\") === this.element) {\n                return;\n            }\n            this.dragging = false;\n            this.element.classList.remove(\"drop-zone\");\n        };\n        this.onFileInputChange = () => {\n            var _a;\n            if ((_a = this.fileInput.files) === null || _a === void 0 ? void 0 : _a.length) {\n                this.file = this.fileInput.files[0];\n            }\n            this.renderWidget();\n        };\n        this.onImagePreviewClick = (e) => {\n            if (e && e.target) {\n                const targetElement = e.target;\n                if (targetElement.closest(\".uuw-delete-icon\")) {\n                    const element = targetElement.closest(\".uuw-image-preview\");\n                    return this.performDeleteImage(element);\n                }\n                else if (targetElement.closest(\".uuw-preview-icon\")) {\n                    const element = targetElement.closest(\".uuw-image-preview\");\n                    return this.performPreviewImage(element);\n                }\n            }\n            this.fileInput.click();\n        };\n        // get main elements\n        this.element = element;\n        const fileInput = element.querySelector(\"input[type=file]\");\n        const checkBoxInput = element.querySelector(\"input[type=checkbox]\");\n        // check if file input exists\n        if (!fileInput) {\n            throw new Error(\"no-file-input-found\");\n        }\n        // store variables\n        this.fileInput = fileInput;\n        this.checkboxInput = checkBoxInput;\n        this.emptyMarker = element.querySelector(\".uuw-empty\");\n        this.canDelete = element.getAttribute(\"data-candelete\") === \"true\";\n        this.dragging = false;\n        // add events\n        this.fileInput.addEventListener(\"change\", this.onFileInputChange);\n        if (this.emptyMarker) {\n            this.emptyMarker.addEventListener(\"click\", this.onEmptyMarkerClick);\n        }\n        this.element.addEventListener(\"dragenter\", this.onDragEnter);\n        this.element.addEventListener(\"dragover\", this.onDragOver);\n        this.element.addEventListener(\"dragleave\", this.onDragLeave);\n        this.element.addEventListener(\"dragend\", this.onDragLeave);\n        this.element.addEventListener(\"drop\", this.onDrop);\n        // init\n        this.raw = element.getAttribute(\"data-raw\");\n        this.file = null;\n        this.renderWidget();\n    }\n    updateCheckBoxAndEmptyState() {\n        if (!this.file && !this.raw) {\n            this.element.classList.remove(\"non-empty\");\n            if (this.checkboxInput) {\n                this.checkboxInput.checked = true;\n            }\n        }\n        else {\n            this.element.classList.add(\"non-empty\");\n            if (this.checkboxInput) {\n                this.checkboxInput.checked = false;\n            }\n        }\n    }\n    renderWidget() {\n        this.updateCheckBoxAndEmptyState();\n        Array.from(this.element.querySelectorAll(\".uuw-image-preview\")).forEach((item) => this.element.removeChild(item));\n        if (this.file) {\n            const url = URL.createObjectURL(this.file);\n            this.element.appendChild((0, Preview_1.renderPreview)(url, this.canDelete, this.canPreview));\n        }\n        else if (this.raw) {\n            this.element.appendChild((0, Preview_1.renderPreview)(this.raw, this.canDelete, this.canPreview));\n        }\n        Array.from(this.element.querySelectorAll(\".uuw-image-preview\")).forEach((item) => item.addEventListener(\"click\", this.onImagePreviewClick));\n    }\n}\nexports.ImageUploaderWidget = ImageUploaderWidget;\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/Widget/ImageUploaderWidget/ImageUploaderWidget.ts?");

/***/ }),

/***/ "./src/Widget/ImageUploaderWidget/index.ts":
/*!*************************************************!*\
  !*** ./src/Widget/ImageUploaderWidget/index.ts ***!
  \*************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports.ImageUploaderWidget = void 0;\nvar ImageUploaderWidget_1 = __webpack_require__(/*! ./ImageUploaderWidget */ \"./src/Widget/ImageUploaderWidget/ImageUploaderWidget.ts\");\nObject.defineProperty(exports, \"ImageUploaderWidget\", ({ enumerable: true, get: function () { return ImageUploaderWidget_1.ImageUploaderWidget; } }));\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/Widget/ImageUploaderWidget/index.ts?");

/***/ }),

/***/ "./src/Widget/PdfUploaderWidget/PdfUploaderWidget.ts":
/*!***********************************************************!*\
  !*** ./src/Widget/PdfUploaderWidget/PdfUploaderWidget.ts ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports.PdfUploaderWidget = void 0;\nconst PreviewModal_1 = __webpack_require__(/*! ../../PreviewModal */ \"./src/PreviewModal/index.ts\");\nconst Preview_1 = __webpack_require__(/*! ../../Preview */ \"./src/Preview/index.ts\");\nclass PdfUploaderWidget {\n    constructor(element) {\n        this.canDelete = false;\n        this.dragging = false;\n        this.canPreview = true;\n        this.raw = null;\n        this.file = null;\n        this.performDeletePdf = (previewElement) => {\n            var _a;\n            (_a = previewElement === null || previewElement === void 0 ? void 0 : previewElement.parentElement) === null || _a === void 0 ? void 0 : _a.removeChild(previewElement);\n            if (this.checkboxInput) {\n                this.checkboxInput.checked = true;\n            }\n            this.fileInput.value = \"\";\n            this.file = null;\n            this.raw = null;\n            this.renderWidget();\n        };\n        this.performPreviewPdf = (previewElement) => {\n            let Pdf = previewElement === null || previewElement === void 0 ? void 0 : previewElement.querySelector(\"canvas\");\n            if (Pdf) {\n                Pdf = Pdf.cloneNode(true);\n                PreviewModal_1.PreviewModal.createPreviewModal(Pdf);\n                PreviewModal_1.PreviewModal.openPreviewModal();\n            }\n        };\n        this.onEmptyMarkerClick = () => {\n            this.fileInput.click();\n        };\n        this.onDrop = (e) => {\n            var _a;\n            e.preventDefault();\n            this.dragging = false;\n            this.element.classList.remove(\"drop-zone\");\n            if ((_a = e.dataTransfer) === null || _a === void 0 ? void 0 : _a.files.length) {\n                this.fileInput.files = e.dataTransfer.files;\n                this.file = this.fileInput.files[0];\n                this.raw = null;\n                this.renderWidget();\n            }\n        };\n        this.onDragEnter = () => {\n            this.dragging = true;\n            this.element.classList.add(\"drop-zone\");\n        };\n        this.onDragOver = (e) => {\n            if (e) {\n                e.preventDefault();\n            }\n        };\n        this.onDragLeave = (e) => {\n            if (e.relatedTarget &&\n                e.relatedTarget.closest(\".uuw-root\") === this.element) {\n                return;\n            }\n            this.dragging = false;\n            this.element.classList.remove(\"drop-zone\");\n        };\n        this.onFileInputChange = () => {\n            var _a;\n            if ((_a = this.fileInput.files) === null || _a === void 0 ? void 0 : _a.length) {\n                this.file = this.fileInput.files[0];\n            }\n            this.renderWidget();\n        };\n        this.onPdfPreviewClick = (e) => {\n            if (e && e.target) {\n                const targetElement = e.target;\n                if (targetElement.closest(\".uuw-delete-icon\")) {\n                    const element = targetElement.closest(\".uuw-pdf-preview\");\n                    return this.performDeletePdf(element);\n                }\n                else if (targetElement.closest(\".uuw-preview-icon\")) {\n                    const element = targetElement.closest(\".uuw-pdf-preview\");\n                    return this.performPreviewPdf(element);\n                }\n            }\n            this.fileInput.click();\n        };\n        // get main elements\n        this.element = element;\n        const fileInput = element.querySelector(\"input[type=file]\");\n        const checkBoxInput = element.querySelector(\"input[type=checkbox]\");\n        // check if file input exists\n        if (!fileInput) {\n            throw new Error(\"no-file-input-found\");\n        }\n        // store variables\n        this.fileInput = fileInput;\n        this.checkboxInput = checkBoxInput;\n        this.emptyMarker = element.querySelector(\".uuw-empty\");\n        this.canDelete = element.getAttribute(\"data-candelete\") === \"true\";\n        this.dragging = false;\n        // add events\n        this.fileInput.addEventListener(\"change\", this.onFileInputChange);\n        if (this.emptyMarker) {\n            this.emptyMarker.addEventListener(\"click\", this.onEmptyMarkerClick);\n        }\n        this.element.addEventListener(\"dragenter\", this.onDragEnter);\n        this.element.addEventListener(\"dragover\", this.onDragOver);\n        this.element.addEventListener(\"dragleave\", this.onDragLeave);\n        this.element.addEventListener(\"dragend\", this.onDragLeave);\n        this.element.addEventListener(\"drop\", this.onDrop);\n        // init\n        this.raw = element.getAttribute(\"data-raw\");\n        this.file = null;\n        this.renderWidget();\n    }\n    updateCheckBoxAndEmptyState() {\n        if (!this.file && !this.raw) {\n            this.element.classList.remove(\"non-empty\");\n            if (this.checkboxInput) {\n                this.checkboxInput.checked = true;\n            }\n        }\n        else {\n            this.element.classList.add(\"non-empty\");\n            if (this.checkboxInput) {\n                this.checkboxInput.checked = false;\n            }\n        }\n    }\n    renderWidget() {\n        this.updateCheckBoxAndEmptyState();\n        Array.from(this.element.querySelectorAll(\".uuw-pdf-preview\")).forEach((item) => this.element.removeChild(item));\n        if (this.file) {\n            const url = URL.createObjectURL(this.file);\n            this.element.appendChild((0, Preview_1.renderPreview)(url, this.canDelete, this.canPreview));\n        }\n        else if (this.raw) {\n            this.element.appendChild((0, Preview_1.renderPreview)(this.raw, this.canDelete, this.canPreview));\n        }\n        Array.from(this.element.querySelectorAll(\".uuw-pdf-preview\")).forEach((item) => item.addEventListener(\"click\", this.onPdfPreviewClick));\n    }\n}\nexports.PdfUploaderWidget = PdfUploaderWidget;\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/Widget/PdfUploaderWidget/PdfUploaderWidget.ts?");

/***/ }),

/***/ "./src/Widget/PdfUploaderWidget/index.ts":
/*!***********************************************!*\
  !*** ./src/Widget/PdfUploaderWidget/index.ts ***!
  \***********************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

eval("\nObject.defineProperty(exports, \"__esModule\", ({ value: true }));\nexports.PdfUploaderWidget = void 0;\nvar PdfUploaderWidget_1 = __webpack_require__(/*! ./PdfUploaderWidget */ \"./src/Widget/PdfUploaderWidget/PdfUploaderWidget.ts\");\nObject.defineProperty(exports, \"PdfUploaderWidget\", ({ enumerable: true, get: function () { return PdfUploaderWidget_1.PdfUploaderWidget; } }));\n\n\n//# sourceURL=webpack://django-universal-uploader-widget/./src/Widget/PdfUploaderWidget/index.ts?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	__webpack_require__("./src/UniversalUploaderWidget.ts");
/******/ 	var __webpack_exports__ = __webpack_require__("./src/UniversalUploaderWidget.scss");
/******/ 	
/******/ })()
;