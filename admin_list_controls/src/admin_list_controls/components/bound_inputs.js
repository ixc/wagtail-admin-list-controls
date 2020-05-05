import React from "react";
import { store } from '../state';

// Once a field has a value, we inject it as an input into the page's search form, so
// that the next search request will persist it. To prevent the url from being cluttered
// by empty inputs, we also assume inputs are removed if they no longer have a value
export class BoundInputs extends React.Component {
    render() {
        const state = store.getState();

        const inputs = [];

        // TODO: reimplement all name/value persistence
        // _.forEach(state.filter_map, filter => {
        //     if (filter.value) {
        //         if (filter.multiple) {
        //             if (filter.value.length) {
        //                 _.forEach(filter.value, (value => {
        //                     inputs.push(<input key={filter.name + value} type="hidden" name={filter.name} value={value} />);
        //                 }));
        //             }
        //         } else {
        //             inputs.push(<input key={filter.name + filter.value} type="hidden" name={filter.name} value={filter.value} />);
        //         }
        //     }
        // });
        //
        return (
            <span className="alc__bound-inputs">{inputs}</span>
        );
    }
}
