import React from "react";
import { render_control } from "./render_control";

export function Button({control}) {
    return (
        <button className="alc__button button" style={control.style}>
            {control.children && control.children.map(control => render_control(control))}
        </button>
    );
}
