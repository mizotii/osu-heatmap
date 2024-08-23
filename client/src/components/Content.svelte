<script>

</script>

<content>
    <slot />
</content>

<style>
    content {
        width: 90%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background-color: #222222;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-radius: 4px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }

    @media (max-width: 600px) {
        content {
            width: 95%;
            padding: 15px;
        }
    }
</style>