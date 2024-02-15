/* eslint-disable */
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
  Base64: { input: any; output: any; }
  /** Date with time (isoformat) */
  DateTime: { input: any; output: any; }
  /** The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID. */
  GlobalID: { input: any; output: any; }
};

export type AssignedTeamRole = Node & {
  __typename?: 'AssignedTeamRole';
  dbId: Scalars['Int']['output'];
  /** The Globally Unique ID of this object */
  id: Scalars['GlobalID']['output'];
  role: Role;
  team: Team;
  user: User;
};

export type Avatar = {
  __typename?: 'Avatar';
  accessory: AvatarPart;
  backgroundColor: Scalars['String']['output'];
  beard: AvatarPart;
  beardColor: Scalars['String']['output'];
  clothing: AvatarPart;
  clothingColor: Scalars['String']['output'];
  eyebrows: AvatarPart;
  eyes: AvatarPart;
  graphic: AvatarPart;
  hairColor: Scalars['String']['output'];
  hatColor: Scalars['String']['output'];
  mouth: AvatarPart;
  nose: AvatarPart;
  shirtText: Scalars['String']['output'];
  skinColor: Scalars['String']['output'];
  svg: Scalars['String']['output'];
  top: AvatarPart;
};

export type AvatarApi = {
  __typename?: 'AvatarAPI';
  accessories: Array<AvatarPart>;
  beards: Array<AvatarPart>;
  clothings: Array<AvatarPart>;
  create: Avatar;
  eyebrows: Array<AvatarPart>;
  eyes: Array<AvatarPart>;
  graphics: Array<AvatarPart>;
  mouths: Array<AvatarPart>;
  noses: Array<AvatarPart>;
  random: Avatar;
  tops: Array<AvatarPart>;
};


export type AvatarApiCreateArgs = {
  avatar: AvatarInput;
};

export type AvatarInput = {
  accessory: Scalars['String']['input'];
  backgroundColor: Scalars['String']['input'];
  beard: Scalars['String']['input'];
  beardColor: Scalars['String']['input'];
  clothing: Scalars['String']['input'];
  clothingColor: Scalars['String']['input'];
  eyebrows: Scalars['String']['input'];
  eyes: Scalars['String']['input'];
  graphic: Scalars['String']['input'];
  hairColor: Scalars['String']['input'];
  hatColor: Scalars['String']['input'];
  mouth: Scalars['String']['input'];
  nose: Scalars['String']['input'];
  shirtText: Scalars['String']['input'];
  skinColor: Scalars['String']['input'];
  top: Scalars['String']['input'];
};

export type AvatarPart = {
  __typename?: 'AvatarPart';
  name: Scalars['String']['output'];
  svg?: Maybe<Scalars['String']['output']>;
};

export type Estimate = Node & {
  __typename?: 'Estimate';
  createdAt: Scalars['DateTime']['output'];
  dbId: Scalars['Int']['output'];
  estimateType: EstimateType;
  estimatedDuration: Scalars['Base64']['output'];
  expectationAverage: Scalars['Base64']['output'];
  expectationOptimistic: Scalars['Base64']['output'];
  expectationPessimistic: Scalars['Base64']['output'];
  /** The Globally Unique ID of this object */
  id: Scalars['GlobalID']['output'];
  task: Task;
  user: User;
};

export type EstimateDatapoint = {
  __typename?: 'EstimateDatapoint';
  actualWork: Scalars['Base64']['output'];
  end: Scalars['DateTime']['output'];
  estimate: Estimate;
  numWorkPeriods: Scalars['Int']['output'];
  start: Scalars['DateTime']['output'];
  value: Scalars['Float']['output'];
};

export type EstimateStatistics = Node & {
  __typename?: 'EstimateStatistics';
  datapoints: Array<EstimateDatapoint>;
  dbId: Scalars['Int']['output'];
  estimateType: EstimateType;
  evaluated: Scalars['DateTime']['output'];
  /** The Globally Unique ID of this object */
  id: Scalars['GlobalID']['output'];
  numDatapoints: Scalars['Int']['output'];
  shiftAverage: Scalars['Float']['output'];
  shiftOptimistic: Scalars['Float']['output'];
  shiftPessimistic: Scalars['Float']['output'];
  sufficient: Scalars['Boolean']['output'];
  user: User;
};

export type EstimateType = Node & {
  __typename?: 'EstimateType';
  dbId: Scalars['Int']['output'];
  defaultShiftAverage: Scalars['Float']['output'];
  defaultShiftOptimistic: Scalars['Float']['output'];
  defaultShiftPessimistic: Scalars['Float']['output'];
  description: Scalars['String']['output'];
  estimateStatistics: Array<EstimateStatistics>;
  /** The Globally Unique ID of this object */
  id: Scalars['GlobalID']['output'];
  maxDatapoints: Scalars['Int']['output'];
  minDatapoints: Scalars['Int']['output'];
  name: Scalars['String']['output'];
  relative: Scalars['Boolean']['output'];
};

export type MovedTaskInput = {
  detached: Scalars['Boolean']['input'];
  orderId: Scalars['Int']['input'];
  taskDbId: Scalars['Int']['input'];
};

export type Mutation = {
  __typename?: 'Mutation';
  login?: Maybe<User>;
  logout?: Maybe<User>;
  project: ProjectMutation;
  user: UserMutation;
};


export type MutationLoginArgs = {
  name: Scalars['String']['input'];
  password: Scalars['String']['input'];
};

export type MutationResult = {
  __typename?: 'MutationResult';
  success: Scalars['Boolean']['output'];
};

/** An object with a Globally Unique ID */
export type Node = {
  /** The Globally Unique ID of this object */
  id: Scalars['GlobalID']['output'];
};

export type Period = {
  __typename?: 'Period';
  end: Scalars['DateTime']['output'];
  start: Scalars['DateTime']['output'];
};

export type Project = Node & {
  __typename?: 'Project';
  children: Array<Project>;
  dbId: Scalars['Int']['output'];
  /** The Globally Unique ID of this object */
  id: Scalars['GlobalID']['output'];
  name: Scalars['String']['output'];
  parent?: Maybe<Project>;
  parents: Array<Project>;
  priorities: Array<Tag>;
  taskStates: Array<Tag>;
  taskTypes: Array<Tag>;
  tasks: Array<Task>;
};


export type ProjectChildrenArgs = {
  recursive?: Scalars['Boolean']['input'];
};

export type ProjectMutation = {
  __typename?: 'ProjectMutation';
  movedTasks: MutationResult;
};


export type ProjectMutationMovedTasksArgs = {
  projectDbId: Scalars['Int']['input'];
  state: TaskState;
  tasks: Array<MovedTaskInput>;
};

export type Query = {
  __typename?: 'Query';
  activeUser?: Maybe<User>;
  avatarApi: AvatarApi;
  dbNode?: Maybe<Node>;
  node?: Maybe<Node>;
  projects: Array<Project>;
  teams: Array<Team>;
  users: Array<User>;
};


export type QueryDbNodeArgs = {
  dbId: Scalars['Int']['input'];
  typename: Scalars['String']['input'];
};


export type QueryNodeArgs = {
  id: Scalars['GlobalID']['input'];
};


export type QueryProjectsArgs = {
  toplevel?: Scalars['Boolean']['input'];
};

export type Role = Node & {
  __typename?: 'Role';
  builtin: Scalars['Boolean']['output'];
  dbId: Scalars['Int']['output'];
  /** The Globally Unique ID of this object */
  id: Scalars['GlobalID']['output'];
  name: Scalars['String']['output'];
  roleType: RoleType;
};

export enum RoleType {
  Global = 'GLOBAL',
  Project = 'PROJECT',
  Team = 'TEAM'
}

export type Schedule = {
  __typename?: 'Schedule';
  actual: Period;
  covers: Period;
  now: Scalars['DateTime']['output'];
  userSchedules: Array<ScheduleUser>;
};

export enum ScheduleMode {
  Average = 'AVERAGE',
  Optimistic = 'OPTIMISTIC',
  Pessimistic = 'PESSIMISTIC'
}

export type SchedulePeriod = {
  __typename?: 'SchedulePeriod';
  color: Scalars['String']['output'];
  period: Period;
  text: Scalars['String']['output'];
};

export type ScheduleRequest = {
  end: Scalars['DateTime']['input'];
  mode?: ScheduleMode;
  start: Scalars['DateTime']['input'];
};

export type ScheduleUser = {
  __typename?: 'ScheduleUser';
  scheduledTasks: Array<SchedulePeriod>;
  timesinks: Array<SchedulePeriod>;
  user: User;
  workedTasks: Array<SchedulePeriod>;
  workingPeriods: Array<Period>;
};

export type Tag = {
  __typename?: 'Tag';
  color: Scalars['String']['output'];
  key?: Maybe<Scalars['String']['output']>;
  text: Scalars['String']['output'];
};

export type Task = Node & {
  __typename?: 'Task';
  active: Scalars['Boolean']['output'];
  activity: Array<TaskActivity>;
  attached: Scalars['Boolean']['output'];
  children: Array<Task>;
  createdAt?: Maybe<Scalars['DateTime']['output']>;
  dbId: Scalars['Int']['output'];
  description: Scalars['String']['output'];
  finishedAt?: Maybe<Scalars['DateTime']['output']>;
  /** The Globally Unique ID of this object */
  id: Scalars['GlobalID']['output'];
  name: Scalars['String']['output'];
  orderId?: Maybe<Scalars['Int']['output']>;
  parent?: Maybe<Task>;
  priority: TaskPriority;
  progress: TaskProgress;
  project: Project;
  state: TaskState;
  tags: Array<Tag>;
  type: TaskType;
};

export type TaskActivity = {
  timestamp: Scalars['DateTime']['output'];
};

export type TaskActivityCreated = TaskActivity & {
  __typename?: 'TaskActivityCreated';
  timestamp: Scalars['DateTime']['output'];
};

export type TaskActivityEstimateAdded = TaskActivity & {
  __typename?: 'TaskActivityEstimateAdded';
  estimate: Estimate;
  timestamp: Scalars['DateTime']['output'];
  user: User;
};

export type TaskActivityFinished = TaskActivity & {
  __typename?: 'TaskActivityFinished';
  timestamp: Scalars['DateTime']['output'];
};

export type TaskActivityWorkperiod = TaskActivity & {
  __typename?: 'TaskActivityWorkperiod';
  duration?: Maybe<Scalars['Base64']['output']>;
  timestamp: Scalars['DateTime']['output'];
  user: User;
};

export enum TaskPriority {
  High = 'HIGH',
  Low = 'LOW',
  Medium = 'MEDIUM',
  VeryHigh = 'VERY_HIGH',
  VeryLow = 'VERY_LOW'
}

export type TaskProgress = {
  __typename?: 'TaskProgress';
  active: Scalars['Boolean']['output'];
  average: Scalars['Int']['output'];
  optimistic: Scalars['Int']['output'];
  pessimistic: Scalars['Int']['output'];
};

export enum TaskState {
  Deferred = 'DEFERRED',
  Discarded = 'DISCARDED',
  Done = 'DONE',
  Hold = 'HOLD',
  Planning = 'PLANNING',
  Request = 'REQUEST',
  Scheduled = 'SCHEDULED'
}

export enum TaskType {
  Adhoc = 'ADHOC',
  Bug = 'BUG',
  Feature = 'FEATURE'
}

export type Team = Node & {
  __typename?: 'Team';
  assignedRoles: Array<AssignedTeamRole>;
  dbId: Scalars['Int']['output'];
  /** The Globally Unique ID of this object */
  id: Scalars['GlobalID']['output'];
  name: Scalars['String']['output'];
  schedule: Schedule;
};


export type TeamScheduleArgs = {
  input: ScheduleRequest;
};

export type User = Node & {
  __typename?: 'User';
  activity: Array<UserActivity>;
  avatar: Avatar;
  dbId: Scalars['Int']['output'];
  estimateStatistics: Array<EstimateStatistics>;
  fullName: Scalars['String']['output'];
  /** The Globally Unique ID of this object */
  id: Scalars['GlobalID']['output'];
  name: Scalars['String']['output'];
  projectSummaries: Array<UserProjectSummary>;
  renderedAvatar: Scalars['String']['output'];
};

export type UserActivity = {
  __typename?: 'UserActivity';
  at: Scalars['DateTime']['output'];
  details: Scalars['String']['output'];
  short: Scalars['String']['output'];
};

export type UserInput = {
  avatar?: InputMaybe<AvatarInput>;
  fullName?: InputMaybe<Scalars['String']['input']>;
  name?: InputMaybe<Scalars['String']['input']>;
};

export type UserMutation = {
  __typename?: 'UserMutation';
  update: MutationResult;
};


export type UserMutationUpdateArgs = {
  user: UserInput;
  userId: Scalars['Int']['input'];
};

export type UserProjectSummary = {
  __typename?: 'UserProjectSummary';
  numTasksDone: Scalars['Int']['output'];
  numTasksOpen: Scalars['Int']['output'];
  project: Project;
  totalDuration: Scalars['Base64']['output'];
};

export type RenderedAvatarQueryVariables = Exact<{
  avatar: AvatarInput;
}>;


export type RenderedAvatarQuery = { __typename?: 'Query', avatarApi: { __typename?: 'AvatarAPI', create: { __typename?: 'Avatar', svg: string } } };

export type AvatarPartsQueryVariables = Exact<{ [key: string]: never; }>;


export type AvatarPartsQuery = { __typename?: 'Query', avatarApi: { __typename?: 'AvatarAPI', tops: Array<(
      { __typename?: 'AvatarPart' }
      & { ' $fragmentRefs'?: { 'AvatarPartFragment': AvatarPartFragment } }
    )>, accessories: Array<(
      { __typename?: 'AvatarPart' }
      & { ' $fragmentRefs'?: { 'AvatarPartFragment': AvatarPartFragment } }
    )>, eyebrows: Array<(
      { __typename?: 'AvatarPart' }
      & { ' $fragmentRefs'?: { 'AvatarPartFragment': AvatarPartFragment } }
    )>, eyes: Array<(
      { __typename?: 'AvatarPart' }
      & { ' $fragmentRefs'?: { 'AvatarPartFragment': AvatarPartFragment } }
    )>, noses: Array<(
      { __typename?: 'AvatarPart' }
      & { ' $fragmentRefs'?: { 'AvatarPartFragment': AvatarPartFragment } }
    )>, mouths: Array<(
      { __typename?: 'AvatarPart' }
      & { ' $fragmentRefs'?: { 'AvatarPartFragment': AvatarPartFragment } }
    )>, beards: Array<(
      { __typename?: 'AvatarPart' }
      & { ' $fragmentRefs'?: { 'AvatarPartFragment': AvatarPartFragment } }
    )>, clothings: Array<(
      { __typename?: 'AvatarPart' }
      & { ' $fragmentRefs'?: { 'AvatarPartFragment': AvatarPartFragment } }
    )>, graphics: Array<(
      { __typename?: 'AvatarPart' }
      & { ' $fragmentRefs'?: { 'AvatarPartFragment': AvatarPartFragment } }
    )> } };

export type AvatarPartFragment = { __typename?: 'AvatarPart', name: string, svg?: string | null } & { ' $fragmentName'?: 'AvatarPartFragment' };

export type RandomAvatarQueryVariables = Exact<{ [key: string]: never; }>;


export type RandomAvatarQuery = { __typename?: 'Query', avatarApi: { __typename?: 'AvatarAPI', random: { __typename?: 'Avatar', skinColor: string, hairColor: string, beardColor: string, hatColor: string, clothingColor: string, backgroundColor: string, shirtText: string, top: { __typename?: 'AvatarPart', name: string }, accessory: { __typename?: 'AvatarPart', name: string }, eyebrows: { __typename?: 'AvatarPart', name: string }, eyes: { __typename?: 'AvatarPart', name: string }, nose: { __typename?: 'AvatarPart', name: string }, mouth: { __typename?: 'AvatarPart', name: string }, beard: { __typename?: 'AvatarPart', name: string }, clothing: { __typename?: 'AvatarPart', name: string }, graphic: { __typename?: 'AvatarPart', name: string } } } };

export type GetProjectsQueryVariables = Exact<{ [key: string]: never; }>;


export type GetProjectsQuery = { __typename?: 'Query', projects: Array<{ __typename?: 'Project', dbId: number, name: string, parent?: { __typename?: 'Project', dbId: number } | null }> };

export type GetTeamsQueryVariables = Exact<{ [key: string]: never; }>;


export type GetTeamsQuery = { __typename?: 'Query', teams: Array<{ __typename?: 'Team', name: string, dbId: number }> };

export type GetUsersQueryVariables = Exact<{ [key: string]: never; }>;


export type GetUsersQuery = { __typename?: 'Query', users: Array<{ __typename?: 'User', dbId: number, name: string, fullName: string, renderedAvatar: string }> };

export type GetProjectBoardQueryVariables = Exact<{
  dbId: Scalars['Int']['input'];
}>;


export type GetProjectBoardQuery = { __typename?: 'Query', project?: { __typename: 'AssignedTeamRole' } | { __typename: 'Estimate' } | { __typename: 'EstimateStatistics' } | { __typename: 'EstimateType' } | { __typename: 'Project', id: any, name: string, tasks: Array<{ __typename?: 'Task', id: any, dbId: number, name: string, state: TaskState, finishedAt?: any | null, orderId?: number | null, attached: boolean, priority: TaskPriority, parent?: { __typename?: 'Task', dbId: number } | null, tags: Array<{ __typename?: 'Tag', text: string, color: string }>, progress: { __typename?: 'TaskProgress', pessimistic: number, average: number, optimistic: number, active: boolean } }>, priorities: Array<{ __typename?: 'Tag', key?: string | null, text: string, color: string }> } | { __typename: 'Role' } | { __typename: 'Task' } | { __typename: 'Team' } | { __typename: 'User' } | null };

export type MoveTasksMutationVariables = Exact<{
  projectDbId: Scalars['Int']['input'];
  state: TaskState;
  tasks: Array<MovedTaskInput> | MovedTaskInput;
}>;


export type MoveTasksMutation = { __typename?: 'Mutation', project: { __typename?: 'ProjectMutation', movedTasks: { __typename?: 'MutationResult', success: boolean } } };

export type GetProjectQueryVariables = Exact<{
  dbId: Scalars['Int']['input'];
}>;


export type GetProjectQuery = { __typename?: 'Query', project?: { __typename?: 'AssignedTeamRole' } | { __typename?: 'Estimate' } | { __typename?: 'EstimateStatistics' } | { __typename?: 'EstimateType' } | { __typename?: 'Project', name: string, children: Array<{ __typename?: 'Project', dbId: number, name: string, parent?: { __typename?: 'Project', dbId: number } | null }>, parents: Array<{ __typename?: 'Project', dbId: number, name: string }> } | { __typename?: 'Role' } | { __typename?: 'Task' } | { __typename?: 'Team' } | { __typename?: 'User' } | null };

export type GetTaskActivityQueryVariables = Exact<{
  dbId: Scalars['Int']['input'];
}>;


export type GetTaskActivityQuery = { __typename?: 'Query', task?: { __typename?: 'AssignedTeamRole' } | { __typename?: 'Estimate' } | { __typename?: 'EstimateStatistics' } | { __typename?: 'EstimateType' } | { __typename?: 'Project' } | { __typename?: 'Role' } | { __typename?: 'Task', activity: Array<{ __typename: 'TaskActivityCreated', timestamp: any } | { __typename: 'TaskActivityEstimateAdded', timestamp: any, estimate: { __typename?: 'Estimate', estimatedDuration: any, expectationOptimistic: any, expectationPessimistic: any, expectationAverage: any, estimateType: { __typename?: 'EstimateType', name: string } }, user: { __typename?: 'User', name: string, fullName: string } } | { __typename: 'TaskActivityFinished', timestamp: any } | { __typename: 'TaskActivityWorkperiod', duration?: any | null, timestamp: any, user: { __typename?: 'User', name: string, fullName: string } }> } | { __typename?: 'Team' } | { __typename?: 'User' } | null };

export type GetTaskOverviewQueryVariables = Exact<{
  dbId: Scalars['Int']['input'];
}>;


export type GetTaskOverviewQuery = { __typename?: 'Query', task?: { __typename: 'AssignedTeamRole' } | { __typename: 'Estimate' } | { __typename: 'EstimateStatistics' } | { __typename: 'EstimateType' } | { __typename: 'Project' } | { __typename: 'Role' } | { __typename: 'Task', name: string, description: string, state: TaskState, priority: TaskPriority, type: TaskType, project: { __typename?: 'Project', priorities: Array<{ __typename?: 'Tag', key?: string | null, text: string, color: string }>, taskStates: Array<{ __typename?: 'Tag', key?: string | null, text: string, color: string }>, taskTypes: Array<{ __typename?: 'Tag', key?: string | null, text: string, color: string }> }, tags: Array<{ __typename?: 'Tag', text: string, color: string }> } | { __typename: 'Team' } | { __typename: 'User' } | null };

export type GetTeamQueryVariables = Exact<{
  dbId: Scalars['Int']['input'];
}>;


export type GetTeamQuery = { __typename?: 'Query', team?: { __typename?: 'AssignedTeamRole' } | { __typename?: 'Estimate' } | { __typename?: 'EstimateStatistics' } | { __typename?: 'EstimateType' } | { __typename?: 'Project' } | { __typename?: 'Role' } | { __typename?: 'Task' } | { __typename?: 'Team', name: string, dbId: number, assignedRoles: Array<{ __typename?: 'AssignedTeamRole', role: { __typename?: 'Role', dbId: number, name: string }, user: { __typename?: 'User', dbId: number, name: string, fullName: string, renderedAvatar: string } }> } | { __typename?: 'User' } | null };

export type GetTeamNamesQueryVariables = Exact<{
  dbId: Scalars['Int']['input'];
}>;


export type GetTeamNamesQuery = { __typename?: 'Query', dbNode?: { __typename?: 'AssignedTeamRole' } | { __typename?: 'Estimate' } | { __typename?: 'EstimateStatistics' } | { __typename?: 'EstimateType' } | { __typename?: 'Project' } | { __typename?: 'Role' } | { __typename?: 'Task' } | { __typename?: 'Team', name: string } | { __typename?: 'User' } | null };

export type ScheduleQueryVariables = Exact<{
  start: Scalars['DateTime']['input'];
  end: Scalars['DateTime']['input'];
  mode: ScheduleMode;
  dbId: Scalars['Int']['input'];
}>;


export type ScheduleQuery = { __typename?: 'Query', team?: { __typename: 'AssignedTeamRole' } | { __typename: 'Estimate' } | { __typename: 'EstimateStatistics' } | { __typename: 'EstimateType' } | { __typename: 'Project' } | { __typename: 'Role' } | { __typename: 'Task' } | { __typename: 'Team', id: any, dbId: number, name: string, schedule: { __typename?: 'Schedule', now: any, covers: { __typename?: 'Period', start: any, end: any }, actual: { __typename?: 'Period', start: any, end: any }, userSchedules: Array<{ __typename?: 'ScheduleUser', user: { __typename?: 'User', fullName: string }, workingPeriods: Array<{ __typename?: 'Period', start: any, end: any }>, timesinks: Array<{ __typename?: 'SchedulePeriod', color: string, text: string, period: { __typename?: 'Period', start: any, end: any } }>, workedTasks: Array<{ __typename?: 'SchedulePeriod', color: string, text: string, period: { __typename?: 'Period', start: any, end: any } }>, scheduledTasks: Array<{ __typename?: 'SchedulePeriod', color: string, text: string, period: { __typename?: 'Period', start: any, end: any } }> }> } } | { __typename: 'User' } | null };

export type GetUserActivityQueryVariables = Exact<{
  dbId: Scalars['Int']['input'];
}>;


export type GetUserActivityQuery = { __typename?: 'Query', user?: { __typename?: 'AssignedTeamRole' } | { __typename?: 'Estimate' } | { __typename?: 'EstimateStatistics' } | { __typename?: 'EstimateType' } | { __typename?: 'Project' } | { __typename?: 'Role' } | { __typename?: 'Task' } | { __typename?: 'Team' } | { __typename?: 'User', activity: Array<{ __typename?: 'UserActivity', at: any, short: string, details: string }> } | null };

export type GetUserQueryVariables = Exact<{
  dbId: Scalars['Int']['input'];
}>;


export type GetUserQuery = { __typename?: 'Query', user?: { __typename?: 'AssignedTeamRole' } | { __typename?: 'Estimate' } | { __typename?: 'EstimateStatistics' } | { __typename?: 'EstimateType' } | { __typename?: 'Project' } | { __typename?: 'Role' } | { __typename?: 'Task' } | { __typename?: 'Team' } | { __typename?: 'User', name: string, fullName: string, renderedAvatar: string, projectSummaries: Array<{ __typename?: 'UserProjectSummary', totalDuration: any, numTasksOpen: number, numTasksDone: number, project: { __typename?: 'Project', id: any, dbId: number, name: string } }>, estimateStatistics: Array<{ __typename?: 'EstimateStatistics', evaluated: any, numDatapoints: number, shiftOptimistic: number, shiftAverage: number, shiftPessimistic: number, sufficient: boolean, estimateType: { __typename?: 'EstimateType', name: string, description: string, minDatapoints: number, maxDatapoints: number, relative: boolean }, datapoints: Array<{ __typename?: 'EstimateDatapoint', value: number, actualWork: any, numWorkPeriods: number, start: any, end: any, estimate: { __typename?: 'Estimate', dbId: number, estimatedDuration: any, task: { __typename?: 'Task', dbId: number, name: string } } }> }> } | null };

export type UserQueryVariables = Exact<{
  userId: Scalars['Int']['input'];
}>;


export type UserQuery = { __typename?: 'Query', user?: { __typename?: 'AssignedTeamRole' } | { __typename?: 'Estimate' } | { __typename?: 'EstimateStatistics' } | { __typename?: 'EstimateType' } | { __typename?: 'Project' } | { __typename?: 'Role' } | { __typename?: 'Task' } | { __typename?: 'Team' } | { __typename?: 'User', name: string, fullName: string, avatar: { __typename?: 'Avatar', skinColor: string, hairColor: string, beardColor: string, hatColor: string, clothingColor: string, backgroundColor: string, shirtText: string, top: { __typename?: 'AvatarPart', name: string }, accessory: { __typename?: 'AvatarPart', name: string }, eyebrows: { __typename?: 'AvatarPart', name: string }, eyes: { __typename?: 'AvatarPart', name: string }, nose: { __typename?: 'AvatarPart', name: string }, mouth: { __typename?: 'AvatarPart', name: string }, beard: { __typename?: 'AvatarPart', name: string }, clothing: { __typename?: 'AvatarPart', name: string }, graphic: { __typename?: 'AvatarPart', name: string } } } | null };

export type SaveUserMutationVariables = Exact<{
  userId: Scalars['Int']['input'];
  user: UserInput;
}>;


export type SaveUserMutation = { __typename?: 'Mutation', user: { __typename?: 'UserMutation', update: { __typename?: 'MutationResult', success: boolean } } };

export const AvatarPartFragmentDoc = {"kind":"Document","definitions":[{"kind":"FragmentDefinition","name":{"kind":"Name","value":"avatarPart"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"AvatarPart"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"svg"}}]}}]} as unknown as DocumentNode<AvatarPartFragment, unknown>;
export const RenderedAvatarDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"renderedAvatar"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"avatar"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"AvatarInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"avatarApi"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"create"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"avatar"},"value":{"kind":"Variable","name":{"kind":"Name","value":"avatar"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"svg"}}]}}]}}]}}]} as unknown as DocumentNode<RenderedAvatarQuery, RenderedAvatarQueryVariables>;
export const AvatarPartsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"avatarParts"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"avatarApi"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"tops"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"avatarPart"}}]}},{"kind":"Field","name":{"kind":"Name","value":"accessories"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"avatarPart"}}]}},{"kind":"Field","name":{"kind":"Name","value":"eyebrows"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"avatarPart"}}]}},{"kind":"Field","name":{"kind":"Name","value":"eyes"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"avatarPart"}}]}},{"kind":"Field","name":{"kind":"Name","value":"noses"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"avatarPart"}}]}},{"kind":"Field","name":{"kind":"Name","value":"mouths"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"avatarPart"}}]}},{"kind":"Field","name":{"kind":"Name","value":"beards"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"avatarPart"}}]}},{"kind":"Field","name":{"kind":"Name","value":"clothings"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"avatarPart"}}]}},{"kind":"Field","name":{"kind":"Name","value":"graphics"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"FragmentSpread","name":{"kind":"Name","value":"avatarPart"}}]}}]}}]}},{"kind":"FragmentDefinition","name":{"kind":"Name","value":"avatarPart"},"typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"AvatarPart"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"svg"}}]}}]} as unknown as DocumentNode<AvatarPartsQuery, AvatarPartsQueryVariables>;
export const RandomAvatarDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"randomAvatar"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"avatarApi"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"random"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"top"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"accessory"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"eyebrows"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"eyes"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"nose"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"mouth"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"beard"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"clothing"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"graphic"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"skinColor"}},{"kind":"Field","name":{"kind":"Name","value":"hairColor"}},{"kind":"Field","name":{"kind":"Name","value":"beardColor"}},{"kind":"Field","name":{"kind":"Name","value":"hatColor"}},{"kind":"Field","name":{"kind":"Name","value":"clothingColor"}},{"kind":"Field","name":{"kind":"Name","value":"backgroundColor"}},{"kind":"Field","name":{"kind":"Name","value":"shirtText"}}]}}]}}]}}]} as unknown as DocumentNode<RandomAvatarQuery, RandomAvatarQueryVariables>;
export const GetProjectsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getProjects"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"projects"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"parent"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbId"}}]}}]}}]}}]} as unknown as DocumentNode<GetProjectsQuery, GetProjectsQueryVariables>;
export const GetTeamsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getTeams"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"teams"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"dbId"}}]}}]}}]} as unknown as DocumentNode<GetTeamsQuery, GetTeamsQueryVariables>;
export const GetUsersDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getUsers"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"users"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"Field","name":{"kind":"Name","value":"renderedAvatar"}}]}}]}}]} as unknown as DocumentNode<GetUsersQuery, GetUsersQueryVariables>;
export const GetProjectBoardDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getProjectBoard"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"project"},"name":{"kind":"Name","value":"dbNode"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"typename"},"value":{"kind":"StringValue","value":"Project","block":false}},{"kind":"Argument","name":{"kind":"Name","value":"dbId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"__typename"}},{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"Project"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"tasks"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"parent"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbId"}}]}},{"kind":"Field","name":{"kind":"Name","value":"tags"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"text"}},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}},{"kind":"Field","name":{"kind":"Name","value":"state"}},{"kind":"Field","name":{"kind":"Name","value":"finishedAt"}},{"kind":"Field","name":{"kind":"Name","value":"orderId"}},{"kind":"Field","name":{"kind":"Name","value":"attached"}},{"kind":"Field","name":{"kind":"Name","value":"progress"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"pessimistic"}},{"kind":"Field","name":{"kind":"Name","value":"average"}},{"kind":"Field","name":{"kind":"Name","value":"optimistic"}},{"kind":"Field","name":{"kind":"Name","value":"active"}}]}},{"kind":"Field","name":{"kind":"Name","value":"priority"}}]}},{"kind":"Field","name":{"kind":"Name","value":"priorities"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"key"}},{"kind":"Field","name":{"kind":"Name","value":"text"}},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]}}]}}]} as unknown as DocumentNode<GetProjectBoardQuery, GetProjectBoardQueryVariables>;
export const MoveTasksDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"moveTasks"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"projectDbId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"state"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"TaskState"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"tasks"}},"type":{"kind":"NonNullType","type":{"kind":"ListType","type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"MovedTaskInput"}}}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"project"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"movedTasks"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"projectDbId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"projectDbId"}}},{"kind":"Argument","name":{"kind":"Name","value":"state"},"value":{"kind":"Variable","name":{"kind":"Name","value":"state"}}},{"kind":"Argument","name":{"kind":"Name","value":"tasks"},"value":{"kind":"Variable","name":{"kind":"Name","value":"tasks"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]}}]} as unknown as DocumentNode<MoveTasksMutation, MoveTasksMutationVariables>;
export const GetProjectDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getProject"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"project"},"name":{"kind":"Name","value":"dbNode"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"typename"},"value":{"kind":"StringValue","value":"Project","block":false}},{"kind":"Argument","name":{"kind":"Name","value":"dbId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"Project"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"children"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"recursive"},"value":{"kind":"BooleanValue","value":true}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"parent"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbId"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"parents"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}}]}}]}}]}}]} as unknown as DocumentNode<GetProjectQuery, GetProjectQueryVariables>;
export const GetTaskActivityDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getTaskActivity"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"task"},"name":{"kind":"Name","value":"dbNode"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"typename"},"value":{"kind":"StringValue","value":"Task","block":false}},{"kind":"Argument","name":{"kind":"Name","value":"dbId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"Task"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"activity"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"__typename"}},{"kind":"Field","name":{"kind":"Name","value":"timestamp"}},{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"TaskActivityEstimateAdded"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"estimate"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"estimateType"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"estimatedDuration"}},{"kind":"Field","name":{"kind":"Name","value":"expectationOptimistic"}},{"kind":"Field","name":{"kind":"Name","value":"expectationPessimistic"}},{"kind":"Field","name":{"kind":"Name","value":"expectationAverage"}}]}},{"kind":"Field","name":{"kind":"Name","value":"user"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}}]}},{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"TaskActivityWorkperiod"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"duration"}},{"kind":"Field","name":{"kind":"Name","value":"user"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}}]}}]}}]}}]}}]}}]} as unknown as DocumentNode<GetTaskActivityQuery, GetTaskActivityQueryVariables>;
export const GetTaskOverviewDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getTaskOverview"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"task"},"name":{"kind":"Name","value":"dbNode"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"typename"},"value":{"kind":"StringValue","value":"Task","block":false}},{"kind":"Argument","name":{"kind":"Name","value":"dbId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"__typename"}},{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"Task"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"state"}},{"kind":"Field","name":{"kind":"Name","value":"priority"}},{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"project"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"priorities"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"key"}},{"kind":"Field","name":{"kind":"Name","value":"text"}},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}},{"kind":"Field","name":{"kind":"Name","value":"taskStates"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"key"}},{"kind":"Field","name":{"kind":"Name","value":"text"}},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}},{"kind":"Field","name":{"kind":"Name","value":"taskTypes"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"key"}},{"kind":"Field","name":{"kind":"Name","value":"text"}},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}},{"kind":"Field","name":{"kind":"Name","value":"tags"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"text"}},{"kind":"Field","name":{"kind":"Name","value":"color"}}]}}]}}]}}]}}]} as unknown as DocumentNode<GetTaskOverviewQuery, GetTaskOverviewQueryVariables>;
export const GetTeamDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getTeam"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"team"},"name":{"kind":"Name","value":"dbNode"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"typename"},"value":{"kind":"StringValue","value":"Team","block":false}},{"kind":"Argument","name":{"kind":"Name","value":"dbId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"Team"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"assignedRoles"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"role"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"user"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"Field","name":{"kind":"Name","value":"renderedAvatar"}}]}}]}}]}}]}}]}}]} as unknown as DocumentNode<GetTeamQuery, GetTeamQueryVariables>;
export const GetTeamNamesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getTeamNames"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbNode"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"typename"},"value":{"kind":"StringValue","value":"Team","block":false}},{"kind":"Argument","name":{"kind":"Name","value":"dbId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"Team"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}}]}}]}}]} as unknown as DocumentNode<GetTeamNamesQuery, GetTeamNamesQueryVariables>;
export const ScheduleDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"schedule"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"start"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DateTime"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"end"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"DateTime"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"mode"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"ScheduleMode"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"team"},"name":{"kind":"Name","value":"dbNode"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"typename"},"value":{"kind":"StringValue","value":"Team","block":false}},{"kind":"Argument","name":{"kind":"Name","value":"dbId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"__typename"}},{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"Team"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"schedule"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"input"},"value":{"kind":"ObjectValue","fields":[{"kind":"ObjectField","name":{"kind":"Name","value":"start"},"value":{"kind":"Variable","name":{"kind":"Name","value":"start"}}},{"kind":"ObjectField","name":{"kind":"Name","value":"end"},"value":{"kind":"Variable","name":{"kind":"Name","value":"end"}}},{"kind":"ObjectField","name":{"kind":"Name","value":"mode"},"value":{"kind":"Variable","name":{"kind":"Name","value":"mode"}}}]}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"now"}},{"kind":"Field","name":{"kind":"Name","value":"covers"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"start"}},{"kind":"Field","name":{"kind":"Name","value":"end"}}]}},{"kind":"Field","name":{"kind":"Name","value":"actual"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"start"}},{"kind":"Field","name":{"kind":"Name","value":"end"}}]}},{"kind":"Field","name":{"kind":"Name","value":"userSchedules"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"user"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}}]}},{"kind":"Field","name":{"kind":"Name","value":"workingPeriods"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"start"}},{"kind":"Field","name":{"kind":"Name","value":"end"}}]}},{"kind":"Field","name":{"kind":"Name","value":"timesinks"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"period"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"start"}},{"kind":"Field","name":{"kind":"Name","value":"end"}}]}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"text"}}]}},{"kind":"Field","name":{"kind":"Name","value":"workedTasks"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"period"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"start"}},{"kind":"Field","name":{"kind":"Name","value":"end"}}]}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"text"}}]}},{"kind":"Field","name":{"kind":"Name","value":"scheduledTasks"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"period"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"start"}},{"kind":"Field","name":{"kind":"Name","value":"end"}}]}},{"kind":"Field","name":{"kind":"Name","value":"color"}},{"kind":"Field","name":{"kind":"Name","value":"text"}}]}}]}}]}}]}}]}}]}}]} as unknown as DocumentNode<ScheduleQuery, ScheduleQueryVariables>;
export const GetUserActivityDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getUserActivity"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"user"},"name":{"kind":"Name","value":"dbNode"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"typename"},"value":{"kind":"StringValue","value":"User","block":false}},{"kind":"Argument","name":{"kind":"Name","value":"dbId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"User"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"activity"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"at"}},{"kind":"Field","name":{"kind":"Name","value":"short"}},{"kind":"Field","name":{"kind":"Name","value":"details"}}]}}]}}]}}]}}]} as unknown as DocumentNode<GetUserActivityQuery, GetUserActivityQueryVariables>;
export const GetUserDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"getUser"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"user"},"name":{"kind":"Name","value":"dbNode"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"typename"},"value":{"kind":"StringValue","value":"User","block":false}},{"kind":"Argument","name":{"kind":"Name","value":"dbId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"dbId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"User"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"Field","name":{"kind":"Name","value":"renderedAvatar"}},{"kind":"Field","name":{"kind":"Name","value":"projectSummaries"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"project"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"totalDuration"}},{"kind":"Field","name":{"kind":"Name","value":"numTasksOpen"}},{"kind":"Field","name":{"kind":"Name","value":"numTasksDone"}}]}},{"kind":"Field","name":{"kind":"Name","value":"estimateStatistics"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"evaluated"}},{"kind":"Field","name":{"kind":"Name","value":"numDatapoints"}},{"kind":"Field","name":{"kind":"Name","value":"shiftOptimistic"}},{"kind":"Field","name":{"kind":"Name","value":"shiftAverage"}},{"kind":"Field","name":{"kind":"Name","value":"shiftPessimistic"}},{"kind":"Field","name":{"kind":"Name","value":"estimateType"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"minDatapoints"}},{"kind":"Field","name":{"kind":"Name","value":"maxDatapoints"}},{"kind":"Field","name":{"kind":"Name","value":"relative"}}]}},{"kind":"Field","name":{"kind":"Name","value":"sufficient"}},{"kind":"Field","name":{"kind":"Name","value":"datapoints"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"value"}},{"kind":"Field","name":{"kind":"Name","value":"actualWork"}},{"kind":"Field","name":{"kind":"Name","value":"numWorkPeriods"}},{"kind":"Field","name":{"kind":"Name","value":"start"}},{"kind":"Field","name":{"kind":"Name","value":"end"}},{"kind":"Field","name":{"kind":"Name","value":"estimate"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"task"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"dbId"}},{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"estimatedDuration"}}]}}]}}]}}]}}]}}]}}]} as unknown as DocumentNode<GetUserQuery, GetUserQueryVariables>;
export const UserDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"user"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"userId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","alias":{"kind":"Name","value":"user"},"name":{"kind":"Name","value":"dbNode"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"typename"},"value":{"kind":"StringValue","value":"User","block":false}},{"kind":"Argument","name":{"kind":"Name","value":"dbId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"userId"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"InlineFragment","typeCondition":{"kind":"NamedType","name":{"kind":"Name","value":"User"}},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"Field","name":{"kind":"Name","value":"avatar"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"top"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"accessory"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"eyebrows"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"eyes"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"nose"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"mouth"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"beard"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"clothing"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"graphic"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"name"}}]}},{"kind":"Field","name":{"kind":"Name","value":"skinColor"}},{"kind":"Field","name":{"kind":"Name","value":"hairColor"}},{"kind":"Field","name":{"kind":"Name","value":"beardColor"}},{"kind":"Field","name":{"kind":"Name","value":"hatColor"}},{"kind":"Field","name":{"kind":"Name","value":"clothingColor"}},{"kind":"Field","name":{"kind":"Name","value":"backgroundColor"}},{"kind":"Field","name":{"kind":"Name","value":"shirtText"}}]}}]}}]}}]}}]} as unknown as DocumentNode<UserQuery, UserQueryVariables>;
export const SaveUserDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"mutation","name":{"kind":"Name","value":"saveUser"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"userId"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"Int"}}}},{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"user"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"UserInput"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"user"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"update"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"userId"},"value":{"kind":"Variable","name":{"kind":"Name","value":"userId"}}},{"kind":"Argument","name":{"kind":"Name","value":"user"},"value":{"kind":"Variable","name":{"kind":"Name","value":"user"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"success"}}]}}]}}]}}]} as unknown as DocumentNode<SaveUserMutation, SaveUserMutationVariables>;