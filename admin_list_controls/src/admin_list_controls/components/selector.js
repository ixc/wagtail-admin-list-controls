import React from "react";
import { render_control } from "./root";

export function Selector({control}) {
    if (control.children) {
        return control.children.map(control => render_control(control));
    }
}
