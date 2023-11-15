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

/***/ "./expense_fe/ts/imageForm.ts":
/*!************************************!*\
  !*** ./expense_fe/ts/imageForm.ts ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\nconst imageInput = document.getElementById(\"imageInput\");\nconst imagePreview = document.getElementById(\"imagePreview\");\nconst imageLink = document.getElementById(\"imageLink\");\nconst imageContainer = document.getElementById(\"imageContainer\");\nconst imageRemoveButton = document.getElementById(\"imageRemoveButton\");\nlet existingImageSrc = null;\nif (!imagePreview.classList.contains(\"d-none\")) {\n    existingImageSrc = imagePreview.src;\n}\nimageInput.onchange = _ => {\n    const [file] = imageInput.files;\n    if (file) {\n        imagePreview.classList.remove(\"d-none\");\n        imagePreview.src = URL.createObjectURL(file);\n        imageLink.href = URL.createObjectURL(file);\n        imageContainer.classList.add(\"input-group\");\n        imageRemoveButton.classList.remove(\"d-none\");\n    }\n};\nimageRemoveButton.onclick = _ => {\n    if (!existingImageSrc) {\n        imagePreview.classList.add(\"d-none\");\n        imagePreview.src = \"\";\n        imageLink.href = \"#\";\n    }\n    else {\n        imagePreview.src = existingImageSrc;\n        imageLink.href = existingImageSrc;\n    }\n    imageContainer.classList.remove(\"input-group\");\n    imageRemoveButton.classList.add(\"d-none\");\n    imageInput.files = null;\n    imageInput.value = \"\";\n};\n\n\n\n//# sourceURL=webpack://expense/./expense_fe/ts/imageForm.ts?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The require scope
/******/ 	var __webpack_require__ = {};
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
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./expense_fe/ts/imageForm.ts"](0, __webpack_exports__, __webpack_require__);
/******/
/******/ })()
;
