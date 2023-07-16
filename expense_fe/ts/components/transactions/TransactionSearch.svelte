<script lang="ts">
    import { keyword } from "./store";
</script>

<div class="col-md-4 col-sm-12 mt-2">
    <input
        class="form-control"
        placeholder="Search transactions..."
        type="search"
        name="search"
        id="search"
        bind:value={$keyword}
    />
</div>
