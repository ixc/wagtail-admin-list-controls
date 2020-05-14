import React, {useState} from "react";
import {SET_VALUE} from '../../constants';
import {store} from '../../state';
import c from "classnames";
import {submit_form} from "../../index";

export function TextFilter({control}) {
    const [value, set_value] = useState(control.value);

    const input_id = `alc__filter-${control.component_id}-${control.name}`;
    return (
        <div
            className={c('alc__filter', 'alc__filter--text', control.extra_classes)}
            style={control.style}
        >
            {/* A form element allows for keyboards to trigger submit events (enter keypress, etc) */}
            <form onSubmit={event => {
                event.preventDefault();
                submit_form();
            }}>
                {control.label
                    ? <label className="alc__filter__label" htmlFor={input_id}>{control.label}</label>
                    : null
                }
                <div className="alc__filter__input-wrap">
                    <input
                        id={input_id}
                        type="text"
                        className="alc__filter__input"
                        value={value}
                        onChange={event => {
                            const value = event.target.value;
                            set_value(value);
                            store.dispatch({
                                type: SET_VALUE,
                                name: control.name,
                                value: value,
                            });
                        }}
                    />
                </div>
            </form>
        </div>
    );
}
