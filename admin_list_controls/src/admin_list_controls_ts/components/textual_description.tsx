import React, {Component} from "react";
import { store } from '../state';
import {State} from '../types';

export class TextualDescription extends Component<{}, {}> {
    render() {
        const state: State = store.getState();
        if (!state.description) {
            return null;
        }
        return (
            <div className="alc__textual-description" dangerouslySetInnerHTML={{__html: state.description}} />
        );
    }
}
