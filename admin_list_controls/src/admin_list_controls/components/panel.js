import React from "react";
import c from 'classnames';
import {render_control} from "./root";
import {store} from "../state";

export function Panel({control}) {
    const state = store.getState();
    let is_collapsed = control.collapsed;
    if (control.ref && control.ref in state.collapsed_panels_by_ref) {
        is_collapsed = state.collapsed_panels_by_ref[control.ref];
    }
    return (
        <div
            className={c('alc__panel', {'is-collapsed': is_collapsed}, control.extra_classes)}
            style={control.style}
        >
            {control.children && control.children.map(control => render_control(control))}
        </div>
    );
}
