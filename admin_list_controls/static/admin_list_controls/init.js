const ui_root = document.createElement('span');
const input_root = document.createElement('span');
let form;

window.$(() => {
    const page_header = document.getElementsByTagName('header')[0];
    page_header.parentNode.insertBefore(ui_root, page_header.nextSibling);

    // If the page already has a form (eg: a ModelAdmin's `search_fields` form), we synchronise
    // our values into that form. This ensures that any form submission will include all values,
    // including wagtail's built-in querying. If the form doesn't exist, we simply create a hidden
    // one to persist data
    form = document.getElementById('changelist-search');
    if (!form) {
        form = document.createElement('form');
        form.style.display = 'none';
        ui_root.parentNode.appendChild(form);
    }
    form.appendChild(input_root);

    init();
});

window.admin_list_controls = {
    controls: [{
        object_type: 'root',
        data: {
            some_prop: 'test prop',
        },
        children: [{
            object_type: 'button',
            data: {
                text: 'first button',
            },
        }, {
            object_type: 'button',
            data: {
                text: 'second button'
            },
        }],
    }],
    components: {},
    register(name, options) {
        admin_list_controls.components[name] = options;
    }
};

admin_list_controls.register('root', {
    template: `
        <div>
            This is the root with a <b>bolded</b> section.
            <br>
            We have {{ some_prop }}.
            <br>
            And <slot></slot>. 
        </div>
    `,
});

admin_list_controls.register('button', {
    template: `
        <button v-on:click="text += 'h'">{{ text }}</button>
    `,
});

function init() {
    function build_control(createElement, control) {
        const options = admin_list_controls.components[control.object_type];
        if (!options) {
            throw new Error(`Cannot find control for ${control.object_type}.`);
        }
        const options_clone = {
            ...options,
            data: () => control.data,
        };


        let rendered_children;
        if (control.children) {
            rendered_children = control.children.map(child_control => {
                return build_control(createElement, child_control);
            });
        }

        return createElement(
            options_clone,
            rendered_children,
        );
    }

    new Vue({
        el: ui_root,
        render: function(createElement) {
            const built_controls = admin_list_controls.controls.map(control => {
                return build_control(createElement, control);
            });
            return createElement('span', {class: 'alc-wrap'}, built_controls);
        }
    });
}