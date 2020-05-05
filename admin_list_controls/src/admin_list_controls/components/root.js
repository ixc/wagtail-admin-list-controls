import React from "react";
import { store } from '../state';
import { render_control } from "./render_control";

export function Root() {
    const state = store.getState();
    return (
        <div className="alc__root">
            {render_control(state.admin_list_controls)}
        </div>
    );
}
