import React, {useState, useEffect} from "react";
import {SET_VALUE} from '../../constants';
import {store} from '../../state';
import c from "classnames";
import {submit_form} from "../../index";

export function DateFilter({control}) {
    const [value, set_value] = useState(control.value);

    const input_id = `alc__filter-${control.component_id}-${control.name}`;
    const inputChange = event => {
        const value = event.target.value;
        set_value(value);
        store.dispatch({
            type: SET_VALUE,
            name: control.name,
            value: value,
        });
    }

    useEffect(() => {
            window.initDateChooser(input_id, {
                "dayOfWeekStart": 1, "format": control.format,
                onChangeDateTime(_, $el) {
                    let el = $el.get(0);
                    el.dispatchEvent(new Event('change'));
                    inputChange({'target': el});
                }
            });
        }, [input_id] // avoid init on every render
    );

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
                        onChange={inputChange}
                    />
                </div>
            </form>
        </div>
    );
}
