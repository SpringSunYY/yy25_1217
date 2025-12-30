<template>
  <div v-if="currentSrc && currentSrc !== ''" :style="`width:${realWidth};height:${realHeight};`">
    <el-image
      :src="`${currentSrc}`"
      fit="cover"
      :style="`width:100%;height:100%;`"
      :preview-src-list="currentSrcList"
      @error="handleImageError"
    >
      <div slot="error" class="image-slot">
        <i class="el-icon-picture-outline"></i>
      </div>
    </el-image>
  </div>
  <div v-else :style="`width:${realWidth};height:${realHeight};background-color:#f5f5f5;display:flex;align-items:center;justify-content:center;border-radius:5px;`" class="image-slot">
    <i class="el-icon-picture-outline" style="font-size:24px;color:#909399;"></i>
  </div>
</template>

<script>
import { isExternal } from "@/utils/validate";

export default {
  name: "ImagePreview",
  props: {
    src: {
      type: [String, null],
      required: false,
      default: null
    },
    width: {
      type: [Number, String],
      default: ""
    },
    height: {
      type: [Number, String],
      default: ""
    }
  },
  data() {
    return {
      useProxyForExternal: false // 标记是否对外部图片使用代理
    };
  },
  computed: {
    realSrc() {
      // 如果 src 为空，返回空字符串
      if (!this.src || this.src === null || this.src === '') {
        return '';
      }
      let real_src = this.src.split(",")[0];
      if (isExternal(real_src)) {
        if (this.useProxyForExternal) {
          // 对外部图片使用代理，避免403错误
          return process.env.VUE_APP_BASE_API + "/common/proxy-image?url=" + encodeURIComponent(real_src);
        }
        return real_src;
      }
      return process.env.VUE_APP_BASE_API + real_src;
    },
    realSrcList() {
      // 如果 src 为空，返回空数组
      if (!this.src || this.src === null || this.src === '') {
        return [];
      }
      let real_src_list = this.src.split(",");
      let srcList = [];
      real_src_list.forEach(item => {
        if (isExternal(item)) {
          if (this.useProxyForExternal) {
            return srcList.push(process.env.VUE_APP_BASE_API + "/common/proxy-image?url=" + encodeURIComponent(item));
          }
          return srcList.push(item);
        }
        return srcList.push(process.env.VUE_APP_BASE_API + item);
      });
      return srcList;
    },
    currentSrc() {
      // 如果 src 为空，返回空字符串
      if (!this.src || this.src === null || this.src === '') {
        return '';
      }
      let real_src = this.src.split(",")[0];
      if (isExternal(real_src)) {
        if (this.useProxyForExternal) {
          return process.env.VUE_APP_BASE_API + "/common/proxy-image?url=" + encodeURIComponent(real_src);
        }
        return real_src;
      }
      return process.env.VUE_APP_BASE_API + real_src;
    },
    currentSrcList() {
      // 如果 src 为空，返回空数组
      if (!this.src || this.src === null || this.src === '') {
        return [];
      }
      let real_src_list = this.src.split(",");
      let srcList = [];
      real_src_list.forEach(item => {
        if (isExternal(item)) {
          if (this.useProxyForExternal) {
            return srcList.push(process.env.VUE_APP_BASE_API + "/common/proxy-image?url=" + encodeURIComponent(item));
          }
          return srcList.push(item);
        }
        return srcList.push(process.env.VUE_APP_BASE_API + item);
      });
      return srcList;
    },
    realWidth() {
      return typeof this.width == "string" ? this.width : `${this.width}px`;
    },
    realHeight() {
      return typeof this.height == "string" ? this.height : `${this.height}px`;
    }
  },
  methods: {
    handleImageError() {
      // 当外部图片加载失败时，切换到代理模式
      if (!this.useProxyForExternal && this.src && this.src !== null && this.src !== '') {
        const real_src = this.src.split(",")[0];
        if (isExternal(real_src)) {
          this.useProxyForExternal = true;
        }
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.el-image {
  border-radius: 5px;
  background-color: #ebeef5;
  box-shadow: 0 0 5px 1px #ccc;
  ::v-deep .el-image__inner {
    transition: all 0.3s;
    cursor: pointer;
    &:hover {
      transform: scale(1.2);
    }
  }
  ::v-deep .image-slot {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    color: #909399;
    font-size: 30px;
  }
}
</style>
