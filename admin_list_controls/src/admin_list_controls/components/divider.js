import React from "react";
import c from "classnames";

export function Divider({control}) {
    return (
        <div
            className={c('alc__divider', control.extra_classes)}
            style={control.style}
        >
            <hr />
        </div>
    );
}
