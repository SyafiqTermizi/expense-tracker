<script lang="ts">
    import { keyword } from "./store";
</script>

<input
    class="form-control form-control-sm"
    placeholder="Search transactions..."
    type="search"
    name="search"
    id="search"
    bind:value={$keyword}
/>
