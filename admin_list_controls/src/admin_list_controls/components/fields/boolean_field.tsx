import React, {Component} from "react";
import { store, HANDLE_FIELD_CHANGE } from '../../state';
import {BooleanFilter} from "../../types";


export interface BooleanFieldProps {
    field: BooleanFilter;
}

export class BooleanField extends Component<BooleanFieldProps, {}> {
    render() {
        const { field } = this.props;

        const input_id = 'boolean-field-' + field.name;

        return (
            <div className="alc__field alc__field--boolean">
                <label className="alc__filter__label" htmlFor={input_id}>{field.label}</label>
                <div className="alc__filter__input-wrap">
                    <input
                        id={input_id}
                        type="checkbox"
                        className="alc__filter__input"
                        checked={field.value as boolean}
                        onChange={event => store.dispatch({
                            type: HANDLE_FIELD_CHANGE,
                            name: field.name,
                            value: event.target.checked,
                        })}
                    />
                </div>
            </div>
        );
    }
}
