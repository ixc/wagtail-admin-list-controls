import React from "react";
import ReactDOM from "react-dom";
import { store } from './state';
import { Root } from './components/root';
import { BoundInputs } from './components/bound_inputs';
import "./styles.scss";

declare global {
    interface Window {
        $: (cb: () => void) => void;
    }
}

const ui_root = document.createElement('span');
const input_root = document.createElement('span');

let form: HTMLFormElement;
window.$(() => {
    const page_header = document.getElementsByTagName('header')[0];
    page_header.parentNode.insertBefore(ui_root, page_header.nextSibling);

    // If the page already has a form (eg: a ModelAdmin's `search_fields` form), we synchronise
    // our values into that form. This ensures that any form submission will include all values,
    // including wagtail's built-in querying. If the form doesn't exist, we simply create a hidden
    // one to persist data
    form = (document.getElementById('changelist-search') as null | HTMLFormElement);
    if (!form) {
        form = document.createElement('form');
        form.style.display = 'none';
        ui_root.parentNode.appendChild(form);
    }
    form.appendChild(input_root);

    store.subscribe(mount);
    mount();
});

function mount(cb?: () => void) {
    ReactDOM.render(<Root />, ui_root);
    ReactDOM.render(<BoundInputs />, input_root, cb);
}

export function submit_search() {
    mount(() => {
        form.submit();
    });
}
