/*! highlightjs-copy-button v1.0.5 */
(function (w) {
    'use strict';

    var BLOCK_NAME = 'hljs-button',
        LN_CLASS = 'hljs-ln-code',
        TEXT_COPY = " ",
        TEXT_ERROR = 'Error',
        TEXT_COPIED = 'Copied';

    // https://wcoder.github.io/notes/string-format-for-string-formating-in-javascript
    String.prototype.format = String.prototype.f = function () {
        var args = arguments;
        return this.replace(/\{(\d+)\}/g, function(m, n){
            return args[n] ? args[n] : m;
        });
    };

    if (typeof w.hljs === 'undefined') {
        console.error('highlight.js not detected!');
    } else {
        w.hljs.initCopyButtonOnLoad = onLoad;
        w.hljs.addCopyButton = addCopyButton;
        w.hljs.copyCode = copyCode;

    }

    function copyCode(event) {
        var target = event.target || event.srcElement;
        if (target.className === BLOCK_NAME) {
            event.preventDefault();

            var el = document.getElementById('post-id-target');
            if (!el) {
                el = document.createElement("textarea");
                el.style.position = "absolute";
                el.style.left = "-9999px";
                el.style.top = "0";
                el.id = 'hljs-copy-el';
                document.body.appendChild(el);
            }
            el.textContent = event.currentTarget.innerText.removeBlankLines();
            el.select();

            try {
                var successful = document.execCommand('copy');
                target.dataset.title = successful ? TEXT_COPIED : TEXT_ERROR;
                if (successful) {
                    setTimeout(function () {
                        target.dataset.title = TEXT_COPY;
                    }, 2000);
                }
            } catch (err) {
                target.dataset.title = TEXT_ERROR;
            }
        }
    }

    function onLoad () {
        if (document.readyState === 'complete') {
            documentReady();
        } else {
            w.addEventListener('DOMContentLoaded', documentReady);
        }
    }

    function documentReady () {
        try {
            var blocks = document.querySelectorAll('code.hljs');

            for (var i in blocks) {
                if (blocks.hasOwnProperty(i)) {
                    addCopyButton(blocks[i]);
                }
            }
        } catch (e) {
            console.error('CopyButton error: ', e);
        }
    }

    function addCopyButton (element) {
        if (typeof element !== 'object') {
            return;
        }

        setTimeout(()=>{
            element.innerHTML = element.innerHTML + (`<div class="${BLOCK_NAME}" data-title="${TEXT_COPY}"></div>`);
            element.setAttribute('onclick', "hljs.copyCode(event)");
        },0)
    }

}(window));