import React from "react";
import c from 'classnames';

export function Icon({control}) {
    return (
        <i className={c('alc__icon', control.classes)} style={control.style} />
    );
}
