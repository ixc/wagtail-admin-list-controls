import React, {Component} from "react";
import { store, HANDLE_FIELD_CHANGE } from '../../state';
import {StringFilter} from "../../types";

export interface StringFieldProps {
    field: StringFilter;
}

export class StringField extends Component<StringFieldProps, {}> {
    render() {
        const { field } = this.props;
        return (
            <div className="alc__field alc__field--string">
                <label className="alc__filter__label">
                    {field.label}
                    <input
                        type="text"
                        className="alc__filter__input"
                        value={field.value as string}
                        onChange={event => store.dispatch({
                            type: HANDLE_FIELD_CHANGE,
                            name: field.name,
                            value: event.target.value,
                        })}
                    />
                </label>
            </div>
        );
    }
}
