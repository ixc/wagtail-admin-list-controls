import React from "react";
import c from "classnames";
import _ from "lodash";
import {REMOVE_ALL_VALUES, SUBMIT_FORM} from "../constants";
import {store} from "../state";
import {create_action} from "../actions";

export function Summary({control}) {
    if (!control.summary || !control.summary.length) {
        return null;
    }

    const summary = _.sortBy(control.summary, obj => obj.group_name);
    const grouped_summary = _.groupBy(summary, 'group_name')

    console.log(summary, grouped_summary)

    return (
        <div
            className={c('alc__summary', control.extra_classes)}
            style={control.style}
        >
            {_.map(grouped_summary, (summary, group_name) => {
                return (
                    <div key={group_name} className="alc__summary__group">
                        <div className="alc__summary__group__name">{group_name}</div>
                        {summary.map((obj, i) => {
                            const onClick = () => {
                                if (obj.action) {
                                    obj.action.forEach(action => {
                                        store.dispatch(create_action(action));
                                    });
                                }
                            }

                            let label = obj.label;
                            let value = obj.display_value || obj.value;

                            if (value === true) {
                                // Don't render the value for boolean filters
                                value = null;
                            } else if (label && value) {
                                label += ': '
                            }

                            return (
                                <div key={i} className="alc__summary__detail">
                                    <button
                                        className="alc__summary__detail__button"
                                        onClick={onClick}
                                    >
                                        {label
                                            ? <span className="alc__summary__detail__label">{label}</span>
                                            : null
                                        }
                                        {value
                                            ? <span className="alc__summary__detail__value">{value}</span>
                                            : null
                                        }
                                        <span className="alc__summary__detail__icon-wrap">
                                            <i className="alc__summary__detail__icon icon icon-cross" />
                                        </span>
                                    </button>
                                </div>
                            );
                        })}
                    </div>
                );
            })}
            {control.reset_label && summary.length > 1
                ? (
                    <div className="alc__summary__reset">
                        <button
                            className="alc__summary__reset__button"
                            onClick={() => {
                                store.dispatch({type: REMOVE_ALL_VALUES});
                                store.dispatch({type: SUBMIT_FORM});
                            }}
                        >
                            {control.reset_label}
                            <i className="alc__summary__reset__icon icon icon-cross" />
                        </button>
                    </div>
                )
                : null
            }
        </div>
    );
}
