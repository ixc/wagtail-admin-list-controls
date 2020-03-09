import React, {Component} from "react";
import c from 'classnames';
import { TabContent } from './tab_content';
import { store, SELECT_SORT } from '../state';
import { submit_search } from "../index";
import {State} from "../types";

export class Sorts extends Component<{}, {}> {
    render() {
        const state: State = store.getState();

        if (!state.has_sorts) {
            return null;
        }

        return (
            <TabContent show_content={state.show_sorts}>
                <div className="alc__sorts">
                    {state.sorts.map((sort, i) => {
                        return (
                            <div key={i} className={c('alc__sorts__sort', {'is-selected': sort.is_selected})}>
                                <button
                                    className="button alc__sorts__button"
                                    onClick={() => {
                                        store.dispatch({type: SELECT_SORT, sort});
                                        submit_search();
                                    }}
                                >
                                    {sort.label}
                                </button>
                            </div>
                        );
                    })}
                </div>
            </TabContent>
        );
    }
}
