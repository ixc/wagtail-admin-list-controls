import React, {Component} from "react";
import { store } from '../state';
import {State} from "../types";

export class Reset extends Component<{}, {}> {
    render() {
        const state: State = store.getState();
        if (!state.show_reset_button) {
            return null;
        }

        return (
            <div className="alc__filter-reset">
                <button className="button alc__filter-reset__button">
                    <a href={window.location.pathname}>
                        <i className="icon-fa icon-fa-times-circle" />
                        Reset
                    </a>
                </button>
            </div>
        );
    }
}
