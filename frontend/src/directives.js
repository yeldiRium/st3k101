const directives = [
    {
        name: "click-outside",
        config: {
            priority: 700,
            bind() {
                this.event = function (event) {
                    console.log('emitting event');
                    this.vm.$emit(self.expression, event)
                };
                this.el.addEventListener('click', this.stopProp);
                document.body.addEventListener('click', this.event);
            },

            unbind() {
                console.log('unbind');
                this.el.removeEventListener('click', this.stopProp);
                document.body.removeEventListener('click', this.event);
            },
            stopProp(event) {
                event.stopPropagation();
            }
        }
    }
];

export default directives;