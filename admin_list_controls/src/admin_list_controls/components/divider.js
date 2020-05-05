import React from "react";

export function Divider({control}) {
    return (
        <div className="alc__divider" style={control.style}>
            <hr />
        </div>
    );
}
