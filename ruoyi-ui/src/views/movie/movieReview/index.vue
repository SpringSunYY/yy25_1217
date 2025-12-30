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
      <el-form-item label="评论ID" prop="reviewId">
        <el-input
          v-model="queryParams.reviewId"
          placeholder="请输入评论ID"
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
      <el-form-item label="评论类型" prop="type">
        <el-select v-model="queryParams.type" placeholder="请选择评论类型" clearable>
          <el-option
            v-for="dict in dict.type.review_type"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="用户名" prop="userName">
        <el-input
          v-model="queryParams.userName"
          placeholder="请输入用户名"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="星级" prop="ratingStar">
        <el-input
          v-model="queryParams.ratingStar"
          placeholder="请输入星级"
          clearable
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="时间" prop="commentTime">
        <el-date-picker
          v-model="dateRangeCommentTime"
          value-format="yyyy-MM-dd"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="影评标题" prop="reviewTitle">
        <el-input
          v-model="queryParams.reviewTitle"
          placeholder="请输入影评标题"
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
          v-hasPermi="['movie:movieReview:add']"
        >新增
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="el-icon-edit"
          size="mini"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['movie:movieReview:edit']"
        >修改
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['movie:movieReview:remove']"
        >删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="el-icon-download"
          size="mini"
          @click="handleExport"
          v-hasPermi="['movie:movieReview:export']"
        >导出
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="el-icon-upload2"
          size="mini"
          @click="handleImport"
          v-hasPermi="['movie:movieReview:import']"
        >导入
        </el-button>
      </el-col>
      <right-toolbar :showSearch.sync="showSearch" @queryTable="getList" :columns="columns"></right-toolbar>
    </el-row>

    <el-table :loading="loading" :data="movieReviewList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="编号" :show-overflow-tooltip="true" v-if="columns[0].visible" prop="id"/>
      <el-table-column label="评论ID" align="center" :show-overflow-tooltip="true" v-if="columns[1].visible"
                       prop="reviewId"/>
      <el-table-column label="电影ID" align="center" :show-overflow-tooltip="true" v-if="columns[2].visible"
                       prop="movieId"/>
      <el-table-column label="评论类型" align="center" v-if="columns[3].visible" prop="type">
        <template slot-scope="scope">
          <dict-tag :options="dict.type.review_type" :value="scope.row.type"/>
        </template>
      </el-table-column>
      <el-table-column label="用户名" align="center" :show-overflow-tooltip="true" v-if="columns[4].visible"
                       prop="userName"/>
      <el-table-column label="星级" align="center" :show-overflow-tooltip="true" v-if="columns[5].visible"
                       prop="ratingStar"/>
      <el-table-column label="有用数" align="center" :show-overflow-tooltip="true" v-if="columns[6].visible"
                       prop="votesUp"/>
      <el-table-column label="没用数" align="center" :show-overflow-tooltip="true" v-if="columns[7].visible"
                       prop="votesDown"/>
      <el-table-column label="回应数" align="center" :show-overflow-tooltip="true" v-if="columns[8].visible"
                       prop="repliesCount"/>
      <el-table-column label="时间" align="center" v-if="columns[9].visible" prop="commentTime" width="180">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.commentTime, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="影评标题" align="center" :show-overflow-tooltip="true" v-if="columns[10].visible"
                       prop="reviewTitle"/>
      <el-table-column label="用户头像" align="center" v-if="columns[11].visible" prop="userAvatar" width="100">
        <template slot-scope="scope">
          <image-preview :src="scope.row.userAvatar" :width="50" :height="50"/>
        </template>
      </el-table-column>
      <el-table-column label="内容" align="center" :show-overflow-tooltip="true" v-if="columns[12].visible"
                       prop="content"/>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="text"
            icon="el-icon-edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['movie:movieReview:edit']"
          >修改
          </el-button>
          <el-button
            size="mini"
            type="text"
            icon="el-icon-delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['movie:movieReview:remove']"
          >删除
          </el-button>
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

    <!-- 添加或修改影评信息表对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="评论ID" prop="reviewId">
          <el-input v-model="form.reviewId" placeholder="请输入评论ID"/>
        </el-form-item>
        <el-form-item label="电影ID" prop="movieId">
          <el-input v-model="form.movieId" placeholder="请输入电影ID"/>
        </el-form-item>
        <el-form-item label="评论类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择评论类型">
            <el-option
              v-for="dict in dict.type.review_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="用户名" prop="userName">
          <el-input v-model="form.userName" placeholder="请输入用户名"/>
        </el-form-item>
        <el-form-item label="星级" prop="ratingStar">
          <el-input v-model="form.ratingStar" placeholder="请输入星级"/>
        </el-form-item>
        <el-form-item label="有用数" prop="votesUp">
          <el-input v-model="form.votesUp" placeholder="请输入有用数"/>
        </el-form-item>
        <el-form-item label="没用数" prop="votesDown">
          <el-input v-model="form.votesDown" placeholder="请输入没用数"/>
        </el-form-item>
        <el-form-item label="回应数" prop="repliesCount">
          <el-input v-model="form.repliesCount" placeholder="请输入回应数"/>
        </el-form-item>
        <el-form-item label="时间" prop="commentTime">
          <el-date-picker clearable
                          v-model="form.commentTime"
                          type="date"
                          value-format="yyyy-MM-dd"
                          placeholder="选择时间">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="影评标题" prop="reviewTitle">
          <el-input v-model="form.reviewTitle" placeholder="请输入影评标题"/>
        </el-form-item>
        <el-form-item label="用户头像" prop="userAvatar">
          <image-upload v-model="form.userAvatar"/>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="form.content" placeholder="请输入内容"/>
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
            <el-checkbox v-model="upload.updateSupport"/>
            是否更新已经存在的影评信息表数据
          </div>
          <span>仅允许导入xls、xlsx格式文件。</span>
          <el-link type="primary" :underline="false" style="font-size:12px;vertical-align: baseline;"
                   @click="importTemplate">下载模板
          </el-link>
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


import {
  listMovieReview,
  getMovieReview,
  delMovieReview,
  addMovieReview,
  updateMovieReview
} from "@/api/movie/movieReview";
import {getToken} from "@/utils/auth";

export default {
  name: "MovieReview",
  dicts: ['review_type'],
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
      // 影评信息表表格数据
      movieReviewList: [],
      // 表格列信息
      columns: [
        {key: 0, label: '编号', visible: true},
        {key: 1, label: '评论ID', visible: true},
        {key: 2, label: '电影ID', visible: true},
        {key: 3, label: '评论类型', visible: true},
        {key: 4, label: '用户名', visible: true},
        {key: 5, label: '星级', visible: true},
        {key: 6, label: '有用数', visible: true},
        {key: 7, label: '没用数', visible: true},
        {key: 8, label: '回应数', visible: true},
        {key: 9, label: '时间', visible: true},
        {key: 10, label: '影评标题', visible: true},
        {key: 11, label: '用户头像', visible: true},
        {key: 12, label: '内容', visible: true}
      ],
      // 弹出层标题
      title: "",
      // 是否显示弹出层
      open: false,
      // 时间时间范围
      dateRangeCommentTime: [],
      // 查询参数
      queryParams: {
        pageNum: 1,
        pageSize: 10,
        id: null,
        reviewId: null,
        movieId: null,
        type: null,
        userName: null,
        ratingStar: null,
        commentTime: null,
        reviewTitle: null,
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
        // 是否更新已经存在的影评信息表数据
        updateSupport: 0,
        // 设置上传的请求头部
        headers: {Authorization: "Bearer " + getToken()},
        // 上传的地址
        url: process.env.VUE_APP_BASE_API + "/movie/movieReview/importData"
      },
      // 表单校验
      rules: {
        id: [
          {required: true, message: "编号不能为空", trigger: "blur"}
        ],
        reviewId: [
          {required: true, message: "评论ID不能为空", trigger: "blur"}
        ],
        movieId: [
          {required: true, message: "电影ID不能为空", trigger: "blur"}
        ]
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    /** 查询影评信息表列表 */
    getList() {
      this.loading = true;
      this.queryParams.params = {};
      if (null != this.dateRangeCommentTime && '' != this.dateRangeCommentTime.toString()) {
        this.queryParams.params["begincommentTime"] = this.dateRangeCommentTime[0];
        this.queryParams.params["endcommentTime"] = this.dateRangeCommentTime[1];
      }
      listMovieReview(this.queryParams).then(response => {
        this.movieReviewList = response.rows;
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
        reviewId: null,
        movieId: null,
        type: null,
        userName: null,
        ratingStar: null,
        votesUp: null,
        votesDown: null,
        repliesCount: null,
        commentTime: null,
        reviewTitle: null,
        userAvatar: null,
        content: null
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
      this.dateRangeCommentTime = [];
      this.resetForm("queryForm");
      this.handleQuery();
    },
    // 多选框选中数据
    handleSelectionChange(selection) {
      this.ids = selection.map(item => item.id)
      this.single = selection.length !== 1
      this.multiple = !selection.length
    },
    /** 新增按钮操作 */
    handleAdd() {
      this.reset();
      this.open = true;
      this.title = "添加影评信息表";
    },
    /** 修改按钮操作 */
    handleUpdate(row) {
      this.reset();
      const id = row.id || this.ids
      getMovieReview(id).then(response => {
        this.form = response.data;
        this.open = true;
        this.title = "修改影评信息表";
      });
    },
    /** 提交按钮 */
    submitForm() {
      this.$refs["form"].validate(valid => {
        if (valid) {
          const submitData = this.buildSubmitData();
          if (submitData.id != null) {
            updateMovieReview(submitData).then(response => {
              this.$modal.msgSuccess("修改成功");
              this.open = false;
              this.getList();
            });
          } else {
            addMovieReview(submitData).then(response => {
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
      const movieReviewIds = row.id || this.ids;
      this.$modal.confirm('是否确认删除影评信息表编号为"' + movieReviewIds + '"的数据项？').then(function () {
        return delMovieReview(movieReviewIds);
      }).then(() => {
        this.getList();
        this.$modal.msgSuccess("删除成功");
      }).catch(() => {
      });
    },
    /** 导出按钮操作 */
    handleExport() {
      this.download('movie/movieReview/export', {
        ...this.queryParams
      }, `movieReview_${new Date().getTime()}.xlsx`)
    },
    /** 导入按钮操作 */
    handleImport() {
      this.upload.title = "影评信息表导入";
      this.upload.open = true;
    },
    /** 下载模板操作 */
    importTemplate() {
      this.download(
        "movie/movieReview/importTemplate",
        {},
        "movieReview_template_" + new Date().getTime() + ".xlsx"
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
      this.$alert("<div style='overflow: auto;overflow-x: hidden;max-height: 70vh;padding: 10px 20px 0;'>" + response.msg + "</div>", "导入结果", {dangerouslyUseHTMLString: true});
      this.$modal.closeLoading()
      this.getList();
    },
    buildSubmitData() {
      const data = {...this.form};
      if (data.id !== null && data.id !== undefined && data.id !== "") {
        data.id = parseInt(data.id, 10);
      } else {
        data.id = null;
      }
      if (data.reviewId !== null && data.reviewId !== undefined && data.reviewId !== "") {
        data.reviewId = parseInt(data.reviewId, 10);
      } else {
        data.reviewId = null;
      }
      if (data.movieId !== null && data.movieId !== undefined && data.movieId !== "") {
        data.movieId = parseInt(data.movieId, 10);
      } else {
        data.movieId = null;
      }
      if (data.ratingStar !== null && data.ratingStar !== undefined && data.ratingStar !== "") {
        data.ratingStar = parseInt(data.ratingStar, 10);
      } else {
        data.ratingStar = null;
      }
      if (data.votesUp !== null && data.votesUp !== undefined && data.votesUp !== "") {
        data.votesUp = parseInt(data.votesUp, 10);
      } else {
        data.votesUp = null;
      }
      if (data.votesDown !== null && data.votesDown !== undefined && data.votesDown !== "") {
        data.votesDown = parseInt(data.votesDown, 10);
      } else {
        data.votesDown = null;
      }
      if (data.repliesCount !== null && data.repliesCount !== undefined && data.repliesCount !== "") {
        data.repliesCount = parseInt(data.repliesCount, 10);
      } else {
        data.repliesCount = null;
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
