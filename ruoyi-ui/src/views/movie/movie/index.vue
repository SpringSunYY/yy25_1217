<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryForm" size="small" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="编号" prop="id">
        <el-input
          v-model="queryParams.id"
          placeholder="请输入编号"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="电影ID" prop="movieId">
        <el-input
          v-model="queryParams.movieId"
          placeholder="请输入电影ID"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="名称" prop="title">
        <el-input
          v-model="queryParams.title"
          placeholder="请输入名称"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="评分" prop="rating">
        <el-input
          v-model="queryParams.rating"
          placeholder="请输入评分"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="语言" prop="language">
        <el-input
          v-model="queryParams.language"
          placeholder="请输入语言"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="国家地区" prop="country">
        <el-input
          v-model="queryParams.country"
          placeholder="请输入国家地区"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="导演" prop="directors">
        <el-input
          v-model="queryParams.directors"
          placeholder="请输入导演"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="编剧" prop="writers">
        <el-input
          v-model="queryParams.writers"
          placeholder="请输入编剧"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="主演" prop="actors">
        <el-input
          v-model="queryParams.actors"
          placeholder="请输入主演"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="上映时间" prop="publishDate">
        <el-input
          v-model="queryParams.publishDate"
          placeholder="请输入上映时间"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="上映年份" prop="publishYear">
        <el-input
          v-model="queryParams.publishYear"
          placeholder="请输入上映年份"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="类型" prop="genres">
        <el-input
          v-model="queryParams.genres"
          placeholder="请输入类型"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="el-icon-plus"
          size="mini"
          @click="handleAdd"
          v-hasPermi="['movie:movie:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['movie:movie:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['movie:movie:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['movie:movie:export']"
        >导出</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-upload2"
          size="mini"
          @click="handleImport"
          v-hasPermi="['movie:movie:import']"
        >导入</el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns"></right-toolbar>
    </el-row>

    <el-table :loading="loading" :data="movieList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="编号" :show-overflow-tooltip="true" v-if="columns[0].visible" prop="id" />
      <el-table-column label="电影ID" align="center" :show-overflow-tooltip="true" v-if="columns[1].visible" prop="movieId" />
      <el-table-column label="名称" align="center" :show-overflow-tooltip="true" v-if="columns[2].visible" prop="title" />
      <el-table-column label="评分" align="center" :show-overflow-tooltip="true" v-if="columns[3].visible" prop="rating" />
      <el-table-column label="看过人数" align="center" :show-overflow-tooltip="true" v-if="columns[4].visible" prop="viewCount" />
      <el-table-column label="想看人数" align="center" :show-overflow-tooltip="true" v-if="columns[5].visible" prop="wishCount" />
      <el-table-column label="总影评数" align="center" :show-overflow-tooltip="true" v-if="columns[6].visible" prop="reviewsCount" />
      <el-table-column label="语言" align="center" :show-overflow-tooltip="true" v-if="columns[7].visible" prop="language" />
      <el-table-column label="国家地区" align="center" :show-overflow-tooltip="true" v-if="columns[8].visible" prop="country" />
      <el-table-column label="导演" align="center" :show-overflow-tooltip="true" v-if="columns[9].visible" prop="directors" />
      <el-table-column label="编剧" align="center" :show-overflow-tooltip="true" v-if="columns[10].visible" prop="writers" />
      <el-table-column label="主演" align="center" :show-overflow-tooltip="true" v-if="columns[11].visible" prop="actors" />
      <el-table-column label="片长" align="center" :show-overflow-tooltip="true" v-if="columns[12].visible" prop="duration" />
      <el-table-column label="片长" align="center" :show-overflow-tooltip="true" v-if="columns[13].visible" prop="durationMinute" />
      <el-table-column label="上映日期" align="center" :show-overflow-tooltip="true" v-if="columns[14].visible" prop="pubDate" />
      <el-table-column label="上映时间" align="center" :show-overflow-tooltip="true" v-if="columns[15].visible" prop="publishDate" />
      <el-table-column label="上映年份" align="center" :show-overflow-tooltip="true" v-if="columns[16].visible" prop="publishYear" />
      <el-table-column label="类型" align="center" :show-overflow-tooltip="true" v-if="columns[17].visible" prop="genres" />
      <el-table-column label="剧情简介" align="center" :show-overflow-tooltip="true" v-if="columns[18].visible" prop="summary" />
      <el-table-column label="封面" align="center" v-if="columns[19].visible" prop="coverUrl" width="100">
        <template slot-scope="scope">
          <image-preview :src="scope.row.coverUrl" :width="50" :height="50"/>
        </template>
      </el-table-column>
      <el-table-column label="详情页" align="center" :show-overflow-tooltip="true" v-if="columns[20].visible" prop="detailUrl" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['movie:movie:edit']"
          >修改</el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['movie:movie:remove']"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.pageNum"
      :limit.sync="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改电影信息表对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入名称" />
        </el-form-item>
        <el-form-item label="评分" prop="rating">
          <el-input v-model="form.rating" placeholder="请输入评分" />
        </el-form-item>
        <el-form-item label="看过人数" prop="viewCount">
          <el-input v-model="form.viewCount" placeholder="请输入看过人数" />
        </el-form-item>
        <el-form-item label="想看人数" prop="wishCount">
          <el-input v-model="form.wishCount" placeholder="请输入想看人数" />
        </el-form-item>
        <el-form-item label="总影评数" prop="reviewsCount">
          <el-input v-model="form.reviewsCount" placeholder="请输入总影评数" />
        </el-form-item>
        <el-form-item label="语言" prop="language">
          <el-input v-model="form.language" placeholder="请输入语言" />
        </el-form-item>
        <el-form-item label="国家地区" prop="country">
          <el-input v-model="form.country" placeholder="请输入国家地区" />
        </el-form-item>
        <el-form-item label="导演" prop="directors">
          <el-input v-model="form.directors" placeholder="请输入导演" />
        </el-form-item>
        <el-form-item label="编剧" prop="writers">
          <el-input v-model="form.writers" placeholder="请输入编剧" />
        </el-form-item>
        <el-form-item label="主演" prop="actors">
          <el-input v-model="form.actors" placeholder="请输入主演" />
        </el-form-item>
        <el-form-item label="片长" prop="duration">
          <el-input v-model="form.duration" placeholder="请输入片长" />
        </el-form-item>
        <el-form-item label="片长（分钟）" prop="durationMinute">
          <el-input v-model="form.durationMinute" placeholder="请输入片长（分钟）" />
        </el-form-item>
        <el-form-item label="上映日期" prop="pubDate">
          <el-input v-model="form.pubDate" placeholder="请输入上映日期" />
        </el-form-item>
        <el-form-item label="上映时间" prop="publishDate">
          <el-input v-model="form.publishDate" placeholder="请输入上映时间" />
        </el-form-item>
        <el-form-item label="上映年份" prop="publishYear">
          <el-input v-model="form.publishYear" placeholder="请输入上映年份" />
        </el-form-item>
        <el-form-item label="类型" prop="genres">
          <el-input v-model="form.genres" placeholder="请输入类型" />
        </el-form-item>
        <el-form-item label="剧情简介" prop="summary">
          <el-input v-model="form.summary" placeholder="请输入剧情简介" />
        </el-form-item>
        <el-form-item label="封面" prop="coverUrl">
          <image-upload v-model="form.coverUrl"/>
        </el-form-item>
        <el-form-item label="详情页" prop="detailUrl">
          <el-input v-model="form.detailUrl" placeholder="请输入详情页" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 导入对话框 -->
    <el-dialog :title="upload.title" :visible.sync="upload.open" width="400px" append-to-body>
      <el-upload
        ref="upload"
        :limit="1"
        accept=".xlsx, .xls"
        :headers="upload.headers"
        :action="upload.url + '?updateSupport=' + upload.updateSupport"
        :disabled="upload.isUploading"
        :on-progress="handleFileUploadProgress"
        :on-success="handleFileSuccess"
        :auto-upload="false"
        drag
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip text-center" slot="tip">
          <div class="el-upload__tip" slot="tip">
            <el-checkbox v-model="upload.updateSupport" /> 是否更新已经存在的电影信息表数据
          </div>
          <span>仅允许导入xls、xlsx格式文件。</span>
          <el-link type="primary" :underline="false" style="font-size:12px;vertical-align: baseline;" @click="importTemplate">下载模板</el-link>
        </div>
      </el-upload>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitFileForm">确 定</el-button>
        <el-button @click="upload.open = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>


import { listMovie, getMovie, delMovie, addMovie, updateMovie } from "@/api/movie/movie";
import { getToken } from "@/utils/auth";

export default {
  name: "Movie",
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 显示搜索条件
      showSearch: true,
      // 总条数
      total: 0,
      // 电影信息表表格数据
      movieList: [],
      // 表格列信息
      columns: [
        { key: 0, label: '编号', visible: true },
        { key: 1, label: '电影ID', visible: true },
        { key: 2, label: '名称', visible: true },
        { key: 3, label: '评分', visible: true },
        { key: 4, label: '看过人数', visible: true },
        { key: 5, label: '想看人数', visible: true },
        { key: 6, label: '总影评数', visible: true },
        { key: 7, label: '语言', visible: true },
        { key: 8, label: '国家地区', visible: true },
        { key: 9, label: '导演', visible: true },
        { key: 10, label: '编剧', visible: true },
        { key: 11, label: '主演', visible: true },
        { key: 12, label: '片长', visible: true },
        { key: 13, label: '片长（分钟）', visible: true },
        { key: 14, label: '上映日期', visible: true },
        { key: 15, label: '上映时间', visible: true },
        { key: 16, label: '上映年份', visible: true },
        { key: 17, label: '类型', visible: true },
        { key: 18, label: '剧情简介', visible: true },
        { key: 19, label: '封面', visible: true },
        { key: 20, label: '详情页', visible: true }
      ],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        id: null,
        movieId: null,
        title: null,
        rating: null,
        language: null,
        country: null,
        directors: null,
        writers: null,
        actors: null,
        publishDate: null,
        publishYear: null,
        genres: null,
      },
      // 表单参数
      form: {},
      // 导入参数
      upload: {
        // 是否显示弹出层（导入）
        open: false,
        // 弹出层标题（导入）
        title: "",
        // 是否禁用上传
        isUploading: false,
        // 是否更新已经存在的电影信息表数据
        updateSupport: 0,
        // 设置上传的请求头部
        headers: { Authorization: "Bearer " + getToken() },
        // 上传的地址
        url: process.env.VUE_APP_BASE_API + "/movie/movie/importData"
      },
      // 表单校验
      rules: {
        id: [
          { required: true, message: "编号不能为空", trigger: "blur" }
        ],
        movieId: [
          { required: true, message: "电影ID不能为空", trigger: "blur" }
        ],
        title: [
          { required: true, message: "名称不能为空", trigger: "blur" }
        ]
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询电影信息表列表 */
    getList() {
      this.loading = true;
      listMovie(this.queryParams).then(response => {
        this.movieList = response.rows;
        this.total = response.total;
        this.loading = false;
      });
    },
    // 取消按钮
    cancel() {
      this.open = false;
      this.reset();
    },
    // 表单重置
    reset() {
      this.form = {
        id: null,
        movieId: null,
        title: null,
        rating: null,
        viewCount: null,
        wishCount: null,
        reviewsCount: null,
        language: null,
        country: null,
        directors: null,
        writers: null,
        actors: null,
        duration: null,
        durationMinute: null,
        pubDate: null,
        publishDate: null,
        publishYear: null,
        genres: null,
        summary: null,
        coverUrl: null,
        detailUrl: null
      };
      this.resetForm("form");
    },
    /** 搜索按钮操作 */
    handleQuery() {
      this.queryParams.pageNum = 1;
      this.getList();
    },
    /** 重置按钮操作 */
    resetQuery() {
      this.resetForm("queryForm");
      this.handleQuery();
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.single = selection.length!==1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加电影信息表";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const id = row.id || this.ids
      getMovie(id).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改电影信息表";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          const submitData = this.buildSubmitData();
          if (submitData.id != null) {
            updateMovie(submitData).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addMovie(submitData).then(response => {
              this.$modal.msgSuccess("新增成功");
              this.open = false;
              this.getList();
            });
          }
        }
      });
    },
    /** 删除按钮操作 */
    handleDelete(row) {
      const movieIds = row.id || this.ids;
      this.$modal.confirm('是否确认删除电影信息表编号为"' + movieIds + '"的数据项？').then(function() {
        return delMovie(movieIds);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {});
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('movie/movie/export', {
        ...this.queryParams
      }, `movie_${new Date().getTime()}.xlsx`)
    },
    /** 导入按钮操作 */
    handleImport() {
      this.upload.title = "电影信息表导入";
      this.upload.open = true;
    },
    /** 下载模板操作 */
    importTemplate() {
      this.download(
        "movie/movie/importTemplate",
        {},
        "movie_template_" + new Date().getTime() + ".xlsx"
      );
    },
    // 文件上传中处理
    handleFileUploadProgress(event, file, fileList) {
      this.upload.isUploading = true;
    },
    // 文件上传成功处理
    handleFileSuccess(response, file, fileList) {
      this.upload.open = false;
      this.upload.isUploading = false;
      this.$refs.upload.clearFiles();
      this.$alert("<div style='overflow: auto;overflow-x: hidden;max-height: 70vh;padding: 10px 20px 0;'>" + response.msg + "</div>", "导入结果", { dangerouslyUseHTMLString: true });
      this.$modal.closeLoading()
      this.getList();
    },
    buildSubmitData() {
      const data = { ...this.form };
      if (data.id !== null && data.id !== undefined && data.id !== "") {
        data.id = parseInt(data.id, 10);
      } else {
        data.id = null;
      }
      if (data.movieId !== null && data.movieId !== undefined && data.movieId !== "") {
        data.movieId = parseInt(data.movieId, 10);
      } else {
        data.movieId = null;
      }
      if (data.rating !== null && data.rating !== undefined && data.rating !== "") {
        data.rating = parseFloat(data.rating);
      } else {
        data.rating = null;
      }
      if (data.viewCount !== null && data.viewCount !== undefined && data.viewCount !== "") {
        data.viewCount = parseInt(data.viewCount, 10);
      } else {
        data.viewCount = null;
      }
      if (data.wishCount !== null && data.wishCount !== undefined && data.wishCount !== "") {
        data.wishCount = parseInt(data.wishCount, 10);
      } else {
        data.wishCount = null;
      }
      if (data.reviewsCount !== null && data.reviewsCount !== undefined && data.reviewsCount !== "") {
        data.reviewsCount = parseInt(data.reviewsCount, 10);
      } else {
        data.reviewsCount = null;
      }
      if (data.durationMinute !== null && data.durationMinute !== undefined && data.durationMinute !== "") {
        data.durationMinute = parseInt(data.durationMinute, 10);
      } else {
        data.durationMinute = null;
      }
      if (data.publishYear !== null && data.publishYear !== undefined && data.publishYear !== "") {
        data.publishYear = parseInt(data.publishYear, 10);
      } else {
        data.publishYear = null;
      }
      return data;
    },
    // 提交上传文件
    submitFileForm() {
      this.$modal.loading("导入中请稍后")
      this.$refs.upload.submit();
    }
  }
};
</script>