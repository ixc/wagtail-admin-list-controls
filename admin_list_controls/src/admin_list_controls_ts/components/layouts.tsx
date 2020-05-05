import React, {Component} from "react";
import {SELECT_LAYOUT, store} from '../state';
import {submit_search} from "../index";
import c from 'classnames';
import {State} from "../types";

export class Layouts extends Component<{}, {}> {
    render() {
        const state: State = store.getState();

        if (!state.has_layouts) {
            return null;
        }

        return (
            <div className="alc__layouts">
                {state.layouts.map((layout, i) => {
                    return (
                        <div
                            key={i}
                            className={c('alc__layouts__layout', {
                                'is-selected': layout.is_selected
                            })}
                        >
                            <button
                                className="alc__layouts__layout__button"
                                onClick={() => {
                                    store.dispatch({type: SELECT_LAYOUT, layout});
                                    submit_search();
                                }}
                                title={layout.label}
                            >
                                <i className={layout.icon_class} />
                                <div className="sr-only">{layout.label}</div>
                            </button>
                        </div>
                    )
                })}
            </div>
        );
    }
}
