import React, {Component} from "react";
import { store } from '../state';
import _ from 'lodash';
import {State} from "../types";

// Once a field has a value, we inject it as an input into the page's search form, so
// that the next search request will persist it. To prevent the url from being cluttered
// by empty inputs, we also assume inputs are removed if they no longer have a value
export class BoundInputs extends Component<{}, {}> {
    render() {
        const state: State = store.getState();

        const inputs: JSX.Element[] = [];

        _.forEach(state.filter_map, filter => {
            if (filter.value) {
                if (filter.multiple) {
                    if ((filter.value as string[]).length) {
                        _.forEach((filter.value as string[]), (value => {
                            inputs.push(<input key={filter.name + value} type="hidden" name={filter.name} value={value} />);
                        }));
                    }
                } else {
                    inputs.push(<input key={filter.name + filter.value} type="hidden" name={filter.name} value={(filter.value as string)} />);
                }
            }
        });

        state.sorts.forEach(sort => {
            if (sort.is_selected) {
                inputs.push(<input key={sort.name + sort.value} type="hidden" name={sort.name} value={sort.value} />);
            }
        });

        state.layouts.forEach(layout => {
            if (layout.is_selected) {
                inputs.push(<input key={layout.name + layout.value} type="hidden" name={layout.name} value={layout.value} />);
            }
        });

        return (
            <span className="alc__bound-inputs">{inputs}</span>
        );
    }
}
