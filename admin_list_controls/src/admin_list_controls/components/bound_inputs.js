import React from "react";
import { store } from '../state';

// Once a field has a value, we inject it as an input into the page's search form, so
// that the next search request will persist it. To prevent the url from being cluttered
// by empty inputs, we also assume inputs are removed if they no longer have a value
export function BoundInputs() {
    const state = store.getState();

    const inputs = [];
    _.forEach(state.values, (values, name) => {
        values.forEach((value, i) => {
            if (value) {
                inputs.push(<input key={name + i} type="hidden" name={name} value={value} />);
            }
        });
    });

    return (
        <span className="alc__bound-inputs">{inputs}</span>
    );
}
