import React from "react";
import _ from 'lodash';
import { store, HANDLE_FIELD_CHANGE } from '../../state';

export class RadioField extends React.Component {
    render() {
        const { field } = this.props;

        return (
            <div className="alc__field alc__field--radio">
                <div className="alc__filter__label">{field.label}</div>
                <div className="alc__field__radio-choices clearfix">
                    {field.choices.map(choice => {
                        return (
                            <label key={choice.value} className="alc__filter__radio-choice__label">
                                <input
                                    type="radio"
                                    name={field.name}
                                    value={choice.value}
                                    checked={choice.value === field.value}
                                    onChange={() => store.dispatch({
                                        type: HANDLE_FIELD_CHANGE,
                                        name: field.name,
                                        value: choice.value,
                                    })}
                                    className="alc__field__radio-choice__input"
                                />
                                <span className="alc__filter__radio-choice__label__text">{choice.label}</span>
                            </label>
                        );
                    })}
                </div>
            </div>
        );
    }
}
