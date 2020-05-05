import React from "react";
import { store, HANDLE_FIELD_CHANGE } from '../../state';

export class StringField extends React.Component {
    render() {
        const { field } = this.props;
        return (
            <div className="alc__field alc__field--string">
                <label className="alc__filter__label">
                    {field.label}
                    <input
                        type="text"
                        className="alc__filter__input"
                        value={field.value}
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
