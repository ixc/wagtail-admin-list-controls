import React from "react";
import { render_control } from "./root";

export function ListControls({control}) {
    return (
        <div className="alc__list-controls" style={control.style}>
            {control.children && control.children.map(control => render_control(control))}
        </div>
    );
}
