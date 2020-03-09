import React, {Component} from "react";
import Select from 'react-select';
import _ from 'lodash';
import { store, HANDLE_FIELD_CHANGE } from '../../state';
import {ChoiceFilter} from "../../types";


export interface ChoiceFieldProps {
    field: ChoiceFilter;
}

export class ChoiceField extends Component<ChoiceFieldProps, {}> {
    render() {
        const { field } = this.props;

        let value;
        if (field.value) {
            if (field.multiple) {
                const value_lookup: {[value: string]: boolean} = {};
                (field.value as string[]).forEach(value => value_lookup[value] = true);
                value = field.choices.filter(choice => value_lookup[choice.value]);
            } else {
                value = _.find(field.choices, {value: (field.value as string)});
            }
        }

        const htmlFor = `choice-field-${field.name}`;

        return (
            <div className="alc__field alc__field--choice">
                <label className="alc__filter__label" htmlFor={htmlFor}>
                    {field.label}
                </label>
                <Select
                    id={htmlFor}
                    className="alc__filter__input"
                    value={value}
                    isMulti={field.multiple}
                    isClearable={field.clearable}
                    onChange={(selected: {value: string | string[]}) => {
                        let value;
                        if (field.multiple) {
                            value = _.map(selected, 'value',);
                        } else if (selected) {
                            value = selected.value;
                        } else {
                            value = selected;
                        }
                        store.dispatch({
                            type: HANDLE_FIELD_CHANGE,
                            name: field.name,
                            value: value,
                        })
                    }}
                    options={field.choices}
                    theme={(theme: any) => ({
                      ...theme,
                      colors: {
                        ...theme.colors,
                        primary: '#00b0b1',
                      },
                    })}
                />
            </div>
        );
    }
}
