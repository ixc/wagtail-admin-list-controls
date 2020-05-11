import React, {useState} from "react";
import {SET_VALUE} from '../../constants';
import {store} from '../../state';

export function RadioFilter({control}) {
    const [value, set_value] = useState(control.value);

    return (
        <div className="alc__filter alc__filter--radio">
            {control.label
                ? <label className="alc__filter__label">{control.label}</label>
                : null
            }
            <div className="alc__filter__input-wrap">
                {control.choices.map((choice, i) => {
                    const input_id = `alc__filter-${control.component_id}-${control.name}-${choice[0]}`;
                    return (
                        <div key={`${i}-${choice.value}`} className="alc__filter__radio-choice">
                            <label className="alc__filter__radio-choice__label" htmlFor={input_id}>
                                <input
                                    type="radio"
                                    id={input_id}
                                    name={control.name}
                                    value={choice[0]}
                                    checked={choice[0] === value}
                                    onChange={() => {
                                        set_value(choice[0]);
                                        store.dispatch({
                                            type: SET_VALUE,
                                            name: control.name,
                                            value: choice[0],
                                        })
                                    }}
                                    className="alc__filter__radio-choice__input"
                                />
                                <span className="alc__filter__radio-choice__text">
                                    {choice[1]}
                                </span>
                            </label>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

