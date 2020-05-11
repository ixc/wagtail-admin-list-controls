import React from "react";
import c from "classnames";
import {render_control} from "./root";
import {create_action} from "../actions";
import {store} from "../state";

export function Button({control}) {
    const state = store.getState()

    const onClick = () => {
        if (control.action) {
            control.action.forEach(action => {
                store.dispatch(create_action(action));
            });
        }
    }

    let right_icon = null;
    control.action.forEach(action => {
        if (action.show_panel_toggle_icon) {
            const target_control = state.controls_by_ref[action.ref];
            if (target_control) {
                const collapsed_by_default = target_control.collapsed;
                const ref_has_been_toggled = action.ref in state.collapsed_panels_by_ref;
                if (
                    state.collapsed_panels_by_ref[action.ref] ||
                    (!ref_has_been_toggled && collapsed_by_default)
                ) {
                    right_icon = <i className="alc__icon alc__icon--panel-toggle icon icon-arrow-down" />;
                } else {
                    right_icon = <i className="alc__icon alc__icon--panel-toggle icon icon-arrow-up" />;
                }
            }
        }
    });

    return (
        <button
            className={c('alc__button button', control.extra_classes)}
            onClick={onClick}
            style={control.style}
        >
            {control.children && control.children.map(control => render_control(control))}
            {right_icon}
        </button>
    );
}
