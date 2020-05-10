import React from "react";
import c from "classnames";
import { render_control } from "./root";

export function Selector({control}) {
    return (
        <span
            className={c(
                'alc__selector',
                `alc__selector--${control.selector_type}`,
                control.extra_classes
            )}
        >
            {control.children && control.children.map(control => render_control(control))}
        </span>
    );
}
