import React from "react";
import c from 'classnames';

export function Text({control}) {
    return (
        <span
            className={c('alc__text', `alc__text--size-${control.size}`, control.extra_classes)}
            style={control.style}
        >
            {control.content}
        </span>
    );
}
