import React, {useState} from "react";
import Select from 'react-select';
import _ from 'lodash';
import {SET_VALUE} from '../../constants';
import {store} from '../../state';

export function ChoiceFilter({control}) {
    const choices = [];
    const value_to_choice = Object.create(null);
    _.forEach(control.choices, choice => {
        const choice_obj = {
            value: choice[0],
            label: choice[1],
        };
        choices.push(choice_obj);
        value_to_choice[choice[0]] = choice_obj;
    });

    // Safety checks to ensure the incoming value is white-listed by the back-end
    let initial_value;
    if (control.multiple) {
        initial_value = control.value.map(value => value_to_choice[value])
            .filter(_ => _);
    } else {
        initial_value = value_to_choice[control.value];
    }
    const [value, set_value] = useState(initial_value);

    const input_id = `alc__filter-${control.component_id}-${control.name}`;

    return (
        <div className="alc__filter alc__filter--choice">
            {control.label
                ? <label className="alc__filter__label" htmlFor={input_id}>{control.label}</label>
                : null
            }
            <div className="alc__filter__input-wrap">
                <Select
                    id={input_id}
                    className="alc__filter__input"
                    value={value}
                    isMulti={control.multiple}
                    options={choices}
                    isClearable
                    onChange={selected => {
                        set_value(selected);
                        let selected_value;
                        if (control.multiple) {
                            selected_value = control.multiple
                                ? _.map(selected, 'value')
                                : [selected.value];
                        } else if (selected) {
                            selected_value = selected.value;
                        }
                        store.dispatch({
                            type: SET_VALUE,
                            name: control.name,
                            value: selected_value,
                        });
                    }}
                    theme={theme => ({
                      ...theme,
                      colors: {
                        ...theme.colors,
                        primary: '#00b0b1',
                      },
                    })}
                />
            </div>
        </div>
    );
}
