import React from "react";
import c from 'classnames';
import {render_control} from "./root";

export function Columns({control}) {
    return (
        <div
            className={c('alc__columns', 'clearfix', control.extra_classes)}
            style={control.style}
        >
            {control.children && control.children.map(control => render_control(control))}
        </div>
    );
}
